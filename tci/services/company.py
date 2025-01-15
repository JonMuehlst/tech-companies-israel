from typing import List, Optional

from sqlalchemy import or_

from tci.db.models import Company
from tci.db.postgresql import db


class CompanyService:
    def get_company(self, company_id: int) -> Optional[Company]:
        """Get a single company by ID"""
        with db.get_session() as session:
            return session.query(Company).get(company_id)

    def get_companies(self, search_term: str = None) -> List[Company]:
        """Get all companies, optionally filtered by search term"""
        with db.get_session() as session:
            query = session.query(Company)
            if search_term:
                search = f"%{search_term}%"
                query = query.filter(
                    or_(Company.name.ilike(search), Company.description.ilike(search))
                )
            return query.all()

    def create_company(self, name: str, description: str, website: str) -> Company:
        """Create a new company"""
        with db.get_session() as session:
            company = Company(name=name, description=description, website=website)
            session.add(company)
            session.commit()
            return company

    def update_company(self, company_id: int, **kwargs) -> Optional[Company]:
        """Update an existing company"""
        with db.get_session() as session:
            company = session.query(Company).get(company_id)
            if company:
                for key, value in kwargs.items():
                    setattr(company, key, value)
                session.commit()
            return company

    def delete_company(self, company_id: int) -> bool:
        """Delete a company"""
        with db.get_session() as session:
            company = session.query(Company).get(company_id)
            if company:
                session.delete(company)
                session.commit()
                return True
            return False


company_service = CompanyService()
