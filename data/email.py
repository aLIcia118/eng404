"""
Email validation component following the postal code pattern.
Provides abstract Email base class with concrete validators for different email types.
"""

from abc import ABC, abstractmethod
import re


class Email(ABC):
    """Abstract base class for email validators."""
    
    @abstractmethod
    def __init__(self, email: str):
        """Initialize email validator. Cannot instantiate abstract class."""
        print("Can't init this class!")


class StandardEmail(Email):
    """
    Standard email validator following RFC 5322 simplified pattern.
    Validates basic email format: local@domain
    """
    
    # RFC 5322 simplified pattern for standard email validation
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __init__(self, email: str):
        """
        Initialize standard email validator.
        
        Args:
            email: Email address string to validate
            
        Raises:
            TypeError: If email is not a string
            ValueError: If email format is invalid
        """
        if not isinstance(email, str):
            raise TypeError(f'Bad type for email: {type(email)}')
        
        if not email or len(email.strip()) == 0:
            raise ValueError(f'Email cannot be empty: {email=}')
        
        # Normalize: strip whitespace and convert to lowercase
        normalized = email.strip().lower()
        
        if not re.match(self.EMAIL_PATTERN, normalized):
            raise ValueError(f'Invalid email format: {email=}')
        
        self.email = normalized
    
    def __str__(self):
        return self.email
    
    def __eq__(self, other):
        """Compare emails (case-insensitive)."""
        if isinstance(other, StandardEmail):
            return self.email == other.email
        return False
    
    def get_domain(self):
        """Extract domain from email."""
        return self.email.split('@')[1]
    
    def get_local_part(self):
        """Extract local part (before @) from email."""
        return self.email.split('@')[0]


class UniversityEmail(Email):
    """
    University email validator.
    Validates emails with specific university domain patterns.
    """
    
    # Common university domain patterns
    UNIVERSITY_DOMAINS = [
        'edu',  # Educational institution
        'ac.uk',  # UK academic
        'ac.jp',  # Japanese academic
    ]
    
    def __init__(self, email: str, allowed_domains=None):
        """
        Initialize university email validator.
        
        Args:
            email: Email address string to validate
            allowed_domains: Optional list of allowed domains
            
        Raises:
            TypeError: If email is not a string
            ValueError: If email format is invalid or domain not university
        """
        if not isinstance(email, str):
            raise TypeError(f'Bad type for email: {type(email)}')
        
        if not email or len(email.strip()) == 0:
            raise ValueError(f'Email cannot be empty: {email=}')
        
        # Normalize: strip whitespace and convert to lowercase
        normalized = email.strip().lower()
        
        # Basic format check
        if '@' not in normalized or '.' not in normalized:
            raise ValueError(f'Invalid email format: {email=}')
        
        local, domain = normalized.rsplit('@', 1)
        
        if not local or not domain:
            raise ValueError(f'Invalid email format: {email=}')
        
        # Check if domain is university
        self._validate_university_domain(domain, allowed_domains)
        
        self.email = normalized
    
    def _validate_university_domain(self, domain, allowed_domains):
        """
        Validate that domain is a university domain.
        
        Args:
            domain: Email domain to validate
            allowed_domains: Optional list of allowed domains
            
        Raises:
            ValueError: If domain is not a recognized university domain
        """
        # If allowed_domains provided, check against that list
        if allowed_domains:
            if domain not in allowed_domains:
                raise ValueError(
                    f'Domain {domain} not in allowed domains: {allowed_domains}'
                )
            return
        
        # Check against standard university domain patterns
        is_university = any(domain.endswith(ud) for ud in self.UNIVERSITY_DOMAINS)
        
        if not is_university:
            raise ValueError(
                f'Domain {domain} is not a university domain'
            )
    
    def __str__(self):
        return self.email
    
    def __eq__(self, other):
        """Compare emails (case-insensitive)."""
        if isinstance(other, UniversityEmail):
            return self.email == other.email
        return False
    
    def get_domain(self):
        """Extract domain from email."""
        return self.email.split('@')[1]
    
    def get_local_part(self):
        """Extract local part (before @) from email."""
        return self.email.split('@')[0]


# Test constants
TEST_STANDARD_EMAIL = 'user@example.com'
TEST_UNIVERSITY_EMAIL = 'student@university.edu'


def main():
    """Simple test of email validators."""
    try:
        standard = StandardEmail(TEST_STANDARD_EMAIL)
        print(f'Standard email: {standard}')
        print(f'Domain: {standard.get_domain()}')
        
        uni = UniversityEmail(TEST_UNIVERSITY_EMAIL)
        print(f'University email: {uni}')
    except (TypeError, ValueError) as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
