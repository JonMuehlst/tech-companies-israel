#!/usr/bin/env python
"""Import companies from a CSV file into the database."""
import argparse
import csv
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tci.db.postgresql import db
from tci.db.models import Company


def read_companies_csv(csv_path: Path) -> List[Dict[str, str]]:
    """Read company data from CSV file."""
    companies: List[Dict[str, str]] = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not {'name', 'website'}.issubset(set(reader.fieldnames or [])):
            raise ValueError("CSV must contain 'name' and 'website' columns")
        
        for row in reader:
            companies.append({
                'name': row['name'].strip(),
                'website': row['website'].strip() if row['website'] else None,
                'description': row.get('description', '').strip() or None
            })
    
    return companies


def import_companies(companies: List[Dict[str, str]], dry_run: bool = False) -> None:
    """Import companies into the database."""
    with db.get_session() as session:
        for company_data in companies:
            # Check if company already exists
            existing = session.query(Company).filter(
                Company.name == company_data['name']
            ).first()
            
            if existing:
                print(f"[SKIP] Company already exists: {company_data['name']}")
                continue
            
            company = Company(**company_data)
            session.add(company)
            print(f"[{'WOULD ADD' if dry_run else 'ADD'}] {company_data['name']}")
        
        if not dry_run:
            session.commit()
            print(f"\nSuccessfully imported {len(companies)} companies")
        else:
            session.rollback()
            print(f"\nDry run completed. Would import {len(companies)} companies")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import companies from CSV")
    parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to CSV file containing company data"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be imported without making changes"
    )
    
    args = parser.parse_args()
    
    if not args.csv_file.exists():
        print(f"Error: File not found: {args.csv_file}")
        sys.exit(1)
    
    try:
        companies = read_companies_csv(args.csv_file)
        import_companies(companies, dry_run=args.dry_run)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 