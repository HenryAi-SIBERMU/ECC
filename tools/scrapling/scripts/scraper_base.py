"""
Base Scraper Class
CELIOS ECC Intelligence System

Menyediakan fondasi untuk semua scraper dengan fitur:
- Rate limiting
- Retry logic
- Checkpoint/resume
- Error handling
- Logging
"""

import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import yaml

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper:
    """Base class untuk semua scraper"""
    
    def __init__(
        self,
        name: str,
        config_path: str = "config.yaml",
        delay: Optional[float] = None,
        verbose: bool = False
    ):
        self.name = name
        self.config = self._load_config(config_path)
        self.delay = delay or self.config.get(name, {}).get("delay", 1.0)
        self.logger = self._setup_logger(verbose)
        self.session = self._create_session()
        self.data: List[Dict[str, Any]] = []
        self.checkpoint_path: Optional[Path] = None
        
    def _load_config(self, config_path: str) -> Dict:
        """Load YAML configuration"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config {config_path} not found, using defaults")
            return {}
    
    def _setup_logger(self, verbose: bool) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger(self.name)
        level = logging.DEBUG if verbose else logging.INFO
        logger.setLevel(level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=self.config.get(self.name, {}).get("max_retries", 3),
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set User-Agent
        user_agent = self.config.get(self.name, {}).get(
            "user_agent",
            "CELIOS-ECC-Research/1.0"
        )
        session.headers.update({"User-Agent": user_agent})
        
        return session
    
    def _rate_limit(self):
        """Apply rate limiting delay"""
        time.sleep(self.delay)
    
    def fetch_page(self, url: str, **kwargs) -> requests.Response:
        """
        Fetch single page with error handling
        
        Args:
            url: URL to fetch
            **kwargs: Additional requests arguments
            
        Returns:
            Response object
        """
        timeout = self.config.get(self.name, {}).get("timeout", 30)
        
        try:
            self.logger.debug(f"Fetching: {url}")
            response = self.session.get(url, timeout=timeout, **kwargs)
            response.raise_for_status()
            self._rate_limit()
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            raise
    
    def save_checkpoint(self, checkpoint_path: Optional[Path] = None):
        """Save current state as checkpoint"""
        if checkpoint_path is None:
            checkpoint_path = self.checkpoint_path
        
        if checkpoint_path is None:
            return
        
        checkpoint_data = {
            "scraper": self.name,
            "timestamp": datetime.utcnow().isoformat(),
            "entries_scraped": len(self.data),
            "data": self.data
        }
        
        checkpoint_path = Path(checkpoint_path)
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Checkpoint saved: {checkpoint_path}")
    
    def load_checkpoint(self, checkpoint_path: Path) -> List[Dict]:
        """Load checkpoint and resume scraping"""
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            
            self.data = checkpoint.get("data", [])
            self.logger.info(
                f"Resumed from checkpoint: {len(self.data)} entries loaded"
            )
            return self.data
            
        except FileNotFoundError:
            self.logger.warning("No checkpoint found, starting fresh")
            return []
    
    def export_json(self, output_path: str):
        """Export data to JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Exported {len(self.data)} entries to {output_path}")
    
    def export_csv(self, output_path: str):
        """Export data to CSV using pandas"""
        try:
            import pandas as pd
            
            df = pd.DataFrame(self.data)
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use proper CSV quoting to handle commas and newlines in text
            df.to_csv(
                output_path, 
                index=False, 
                encoding='utf-8-sig',
                quoting=1,  # QUOTE_ALL
                escapechar='\\'
            )
            self.logger.info(f"Exported {len(self.data)} entries to {output_path}")
            
        except ImportError:
            self.logger.error("pandas not installed, cannot export CSV")
    
    def get_data(self) -> List[Dict]:
        """Get scraped data"""
        return self.data
    
    def scrape(self):
        """Override this method in child classes"""
        raise NotImplementedError("Subclass must implement scrape() method")
