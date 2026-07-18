"""
Data Export Utilities
CELIOS ECC Intelligence System

Helper functions untuk export data ke berbagai format
"""

import json
from pathlib import Path
from typing import List, Dict, Any


class DataExporter:
    """Helper class untuk export data"""
    
    @staticmethod
    def to_json(
        data: List[Dict[str, Any]],
        output_path: str,
        indent: int = 2,
        ensure_ascii: bool = False
    ):
        """
        Export data ke JSON
        
        Args:
            data: List of dicts
            output_path: Output file path
            indent: JSON indent level
            ensure_ascii: Whether to escape non-ASCII characters
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    
    @staticmethod
    def to_csv(
        data: List[Dict[str, Any]],
        output_path: str,
        encoding: str = 'utf-8-sig'
    ):
        """
        Export data ke CSV menggunakan pandas
        
        Args:
            data: List of dicts
            output_path: Output file path
            encoding: File encoding (utf-8-sig untuk Excel compatibility)
        """
        try:
            import pandas as pd
            
            df = pd.DataFrame(data)
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_csv(output_path, index=False, encoding=encoding)
            
        except ImportError:
            raise ImportError("pandas required for CSV export. Install: pip install pandas")
    
    @staticmethod
    def to_excel(
        data: List[Dict[str, Any]],
        output_path: str,
        sheet_name: str = "Sheet1"
    ):
        """
        Export data ke Excel menggunakan pandas
        
        Args:
            data: List of dicts
            output_path: Output file path (.xlsx)
            sheet_name: Excel sheet name
        """
        try:
            import pandas as pd
            
            df = pd.DataFrame(data)
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_excel(output_path, index=False, sheet_name=sheet_name, engine='openpyxl')
            
        except ImportError:
            raise ImportError(
                "pandas and openpyxl required for Excel export. "
                "Install: pip install pandas openpyxl"
            )
    
    @staticmethod
    def to_markdown(
        data: List[Dict[str, Any]],
        output_path: str,
        title: str = "Data Export"
    ):
        """
        Export data ke Markdown table
        
        Args:
            data: List of dicts
            output_path: Output file path (.md)
            title: Document title
        """
        if not data:
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get all unique keys
        keys = list(data[0].keys())
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            
            # Header
            f.write("| " + " | ".join(keys) + " |\n")
            f.write("|" + "|".join(["---"] * len(keys)) + "|\n")
            
            # Rows
            for row in data:
                values = [str(row.get(key, "")) for key in keys]
                f.write("| " + " | ".join(values) + " |\n")
    
    @staticmethod
    def summary_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics dari data
        
        Args:
            data: List of dicts
            
        Returns:
            Dict dengan summary statistics
        """
        if not data:
            return {"total_entries": 0}
        
        stats = {
            "total_entries": len(data),
            "fields": list(data[0].keys()),
            "field_count": len(data[0].keys())
        }
        
        # Field completeness
        completeness = {}
        for field in stats["fields"]:
            non_empty = sum(1 for row in data if row.get(field))
            completeness[field] = {
                "filled": non_empty,
                "empty": len(data) - non_empty,
                "percentage": round(non_empty / len(data) * 100, 2)
            }
        
        stats["field_completeness"] = completeness
        
        return stats
