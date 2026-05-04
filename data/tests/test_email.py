"""
Comprehensive test suite for email validation component.
Tests follow the pattern established by test_postalcode.py
"""

import pytest
import data.email as em


# Test constants
TEST_STANDARD_EMAIL = 'user@example.com'
TEST_STANDARD_EMAIL_CAPS = 'User@Example.COM'
TEST_STANDARD_EMAIL_SPACES = '  user@example.com  '
TEST_UNIVERSITY_EMAIL = 'student@university.edu'
TEST_UNIVERSITY_EMAIL_UK = 'scholar@oxford.ac.uk'
TEST_UNIVERSITY_EMAIL_JP = 'researcher@todai.ac.jp'


# ============================================================================
# StandardEmail Tests
# ============================================================================

class TestStandardEmailConstruction:
    """Test StandardEmail construction and validation."""
    
    def test_construct_standard_email(self):
        """Test successful construction of standard email."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL)
        assert isinstance(email, em.StandardEmail)
    
    def test_construct_standard_email_case_normalization(self):
        """Test that email is normalized to lowercase."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL_CAPS)
        assert str(email) == TEST_STANDARD_EMAIL
    
    def test_construct_standard_email_whitespace_strip(self):
        """Test that leading/trailing whitespace is stripped."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL_SPACES)
        assert str(email) == TEST_STANDARD_EMAIL
    
    def test_construct_standard_email_bad_type_int(self):
        """Test TypeError when email is integer."""
        with pytest.raises(TypeError):
            em.StandardEmail(42)
    
    def test_construct_standard_email_bad_type_list(self):
        """Test TypeError when email is list."""
        with pytest.raises(TypeError):
            em.StandardEmail(['user@example.com'])
    
    def test_construct_standard_email_bad_type_none(self):
        """Test TypeError when email is None."""
        with pytest.raises(TypeError):
            em.StandardEmail(None)
    
    def test_construct_standard_email_empty_string(self):
        """Test ValueError when email is empty string."""
        with pytest.raises(ValueError):
            em.StandardEmail('')
    
    def test_construct_standard_email_only_whitespace(self):
        """Test ValueError when email is only whitespace."""
        with pytest.raises(ValueError):
            em.StandardEmail('   ')
    
    def test_construct_standard_email_missing_at(self):
        """Test ValueError when @ symbol is missing."""
        with pytest.raises(ValueError):
            em.StandardEmail('userexample.com')
    
    def test_construct_standard_email_missing_domain(self):
        """Test ValueError when domain is missing."""
        with pytest.raises(ValueError):
            em.StandardEmail('user@')
    
    def test_construct_standard_email_missing_local(self):
        """Test ValueError when local part is missing."""
        with pytest.raises(ValueError):
            em.StandardEmail('@example.com')
    
    def test_construct_standard_email_missing_tld(self):
        """Test ValueError when top-level domain is missing."""
        with pytest.raises(ValueError):
            em.StandardEmail('user@example')
    
    def test_construct_standard_email_invalid_chars(self):
        """Test ValueError with invalid characters."""
        with pytest.raises(ValueError):
            em.StandardEmail('user@@example.com')
    
    def test_construct_standard_email_spaces_in_middle(self):
        """Test ValueError when email has spaces in middle."""
        with pytest.raises(ValueError):
            em.StandardEmail('user name@example.com')
    
    def test_construct_standard_email_special_valid_chars(self):
        """Test that valid special characters are accepted."""
        email = em.StandardEmail('user.name+tag@example.com')
        assert isinstance(email, em.StandardEmail)
    
    def test_construct_standard_email_multiple_dots_local(self):
        """Test email with multiple dots in local part."""
        email = em.StandardEmail('user.first.last@example.com')
        assert isinstance(email, em.StandardEmail)
    
    def test_construct_standard_email_subdomain(self):
        """Test email with subdomain."""
        email = em.StandardEmail('user@mail.example.com')
        assert isinstance(email, em.StandardEmail)
    
    def test_construct_standard_email_hyphen_domain(self):
        """Test email with hyphenated domain."""
        email = em.StandardEmail('user@my-example.com')
        assert isinstance(email, em.StandardEmail)


class TestStandardEmailStringRepresentation:
    """Test string representation of StandardEmail."""
    
    def test_str_standard_email(self):
        """Test __str__ method returns normalized email."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL)
        assert str(email) == TEST_STANDARD_EMAIL
    
    def test_str_standard_email_normalized(self):
        """Test __str__ returns lowercase version."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL_CAPS)
        assert str(email) == TEST_STANDARD_EMAIL


class TestStandardEmailEquality:
    """Test equality comparison of StandardEmail."""
    
    def test_equality_same_email(self):
        """Test two identical emails are equal."""
        email1 = em.StandardEmail(TEST_STANDARD_EMAIL)
        email2 = em.StandardEmail(TEST_STANDARD_EMAIL)
        assert email1 == email2
    
    def test_equality_different_case(self):
        """Test emails with different cases are equal (normalized)."""
        email1 = em.StandardEmail(TEST_STANDARD_EMAIL)
        email2 = em.StandardEmail(TEST_STANDARD_EMAIL_CAPS)
        assert email1 == email2
    
    def test_equality_different_email(self):
        """Test different emails are not equal."""
        email1 = em.StandardEmail(TEST_STANDARD_EMAIL)
        email2 = em.StandardEmail('other@example.com')
        assert email1 != email2
    
    def test_equality_with_non_email(self):
        """Test email is not equal to non-email object."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL)
        assert email != TEST_STANDARD_EMAIL
        assert email != 42


class TestStandardEmailExtraction:
    """Test domain and local part extraction."""
    
    def test_get_domain(self):
        """Test domain extraction."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL)
        assert email.get_domain() == 'example.com'
    
    def test_get_domain_subdomain(self):
        """Test domain extraction with subdomain."""
        email = em.StandardEmail('user@mail.example.com')
        assert email.get_domain() == 'mail.example.com'
    
    def test_get_local_part(self):
        """Test local part extraction."""
        email = em.StandardEmail(TEST_STANDARD_EMAIL)
        assert email.get_local_part() == 'user'
    
    def test_get_local_part_with_plus(self):
        """Test local part extraction with plus addressing."""
        email = em.StandardEmail('user+tag@example.com')
        assert email.get_local_part() == 'user+tag'


# ============================================================================
# UniversityEmail Tests
# ============================================================================

class TestUniversityEmailConstruction:
    """Test UniversityEmail construction and validation."""
    
    def test_construct_university_email_edu(self):
        """Test successful construction with .edu domain."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        assert isinstance(email, em.UniversityEmail)
    
    def test_construct_university_email_ac_uk(self):
        """Test successful construction with .ac.uk domain."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL_UK)
        assert isinstance(email, em.UniversityEmail)
    
    def test_construct_university_email_ac_jp(self):
        """Test successful construction with .ac.jp domain."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL_JP)
        assert isinstance(email, em.UniversityEmail)
    
    def test_construct_university_email_case_normalization(self):
        """Test that email is normalized to lowercase."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL.upper())
        assert str(email) == TEST_UNIVERSITY_EMAIL
    
    def test_construct_university_email_whitespace_strip(self):
        """Test that leading/trailing whitespace is stripped."""
        email = em.UniversityEmail(f'  {TEST_UNIVERSITY_EMAIL}  ')
        assert str(email) == TEST_UNIVERSITY_EMAIL
    
    def test_construct_university_email_bad_type_int(self):
        """Test TypeError when email is integer."""
        with pytest.raises(TypeError):
            em.UniversityEmail(42)
    
    def test_construct_university_email_bad_type_dict(self):
        """Test TypeError when email is dict."""
        with pytest.raises(TypeError):
            em.UniversityEmail({'email': TEST_UNIVERSITY_EMAIL})
    
    def test_construct_university_email_empty_string(self):
        """Test ValueError when email is empty string."""
        with pytest.raises(ValueError):
            em.UniversityEmail('')
    
    def test_construct_university_email_only_whitespace(self):
        """Test ValueError when email is only whitespace."""
        with pytest.raises(ValueError):
            em.UniversityEmail('   ')
    
    def test_construct_university_email_missing_at(self):
        """Test ValueError when @ symbol is missing."""
        with pytest.raises(ValueError):
            em.UniversityEmail('student.university.edu')
    
    def test_construct_university_email_non_university_domain(self):
        """Test ValueError with non-university domain."""
        with pytest.raises(ValueError):
            em.UniversityEmail('user@gmail.com')
    
    def test_construct_university_email_non_university_domain_com(self):
        """Test ValueError with .com domain."""
        with pytest.raises(ValueError):
            em.UniversityEmail('user@example.com')
    
    def test_construct_university_email_custom_allowed_domains(self):
        """Test construction with custom allowed domains."""
        email = em.UniversityEmail(
            'user@school.org',
            allowed_domains=['school.org', 'college.org']
        )
        assert isinstance(email, em.UniversityEmail)
    
    def test_construct_university_email_custom_allowed_domains_reject(self):
        """Test rejection with custom allowed domains."""
        with pytest.raises(ValueError):
            em.UniversityEmail(
                'user@university.edu',
                allowed_domains=['school.org', 'college.org']
            )
    
    def test_construct_university_email_custom_allowed_domains_empty(self):
        """Test construction with multiple custom allowed domains."""
        domains = ['nyc.edu', 'boston.edu', 'cambridge.ac.uk']
        for domain in domains:
            email = em.UniversityEmail(
                f'user@{domain}',
                allowed_domains=domains
            )
            assert isinstance(email, em.UniversityEmail)


class TestUniversityEmailStringRepresentation:
    """Test string representation of UniversityEmail."""
    
    def test_str_university_email(self):
        """Test __str__ method returns normalized email."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        assert str(email) == TEST_UNIVERSITY_EMAIL
    
    def test_str_university_email_normalized(self):
        """Test __str__ returns lowercase version."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL.upper())
        assert str(email) == TEST_UNIVERSITY_EMAIL


class TestUniversityEmailEquality:
    """Test equality comparison of UniversityEmail."""
    
    def test_equality_same_email(self):
        """Test two identical emails are equal."""
        email1 = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        email2 = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        assert email1 == email2
    
    def test_equality_different_case(self):
        """Test emails with different cases are equal (normalized)."""
        email1 = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        email2 = em.UniversityEmail(TEST_UNIVERSITY_EMAIL.upper())
        assert email1 == email2
    
    def test_equality_different_email(self):
        """Test different emails are not equal."""
        email1 = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        email2 = em.UniversityEmail('other@college.edu')
        assert email1 != email2
    
    def test_equality_different_types(self):
        """Test UniversityEmail not equal to StandardEmail."""
        uni_email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        standard = em.StandardEmail(TEST_UNIVERSITY_EMAIL)
        assert uni_email != standard


class TestUniversityEmailExtraction:
    """Test domain and local part extraction."""
    
    def test_get_domain(self):
        """Test domain extraction."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        assert email.get_domain() == 'university.edu'
    
    def test_get_local_part(self):
        """Test local part extraction."""
        email = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        assert email.get_local_part() == 'student'


# ============================================================================
# Abstract Base Class Tests
# ============================================================================

class TestEmailAbstractBase:
    """Test that Email cannot be instantiated."""
    
    def test_cannot_instantiate_abstract_email(self):
        """Test that Email base class cannot be instantiated."""
        with pytest.raises(TypeError):
            em.Email(TEST_STANDARD_EMAIL)


# ============================================================================
# Integration Tests
# ============================================================================

class TestEmailIntegration:
    """Integration tests for email validators."""
    
    def test_multiple_emails_different_types(self):
        """Test creating multiple emails of different types."""
        standard = em.StandardEmail(TEST_STANDARD_EMAIL)
        university = em.UniversityEmail(TEST_UNIVERSITY_EMAIL)
        
        assert str(standard) == TEST_STANDARD_EMAIL
        assert str(university) == TEST_UNIVERSITY_EMAIL
        assert standard != university
    
    def test_email_normalization_consistency(self):
        """Test that email normalization is consistent."""
        email1 = em.StandardEmail('  USER@EXAMPLE.COM  ')
        email2 = em.StandardEmail('user@example.com')
        email3 = em.StandardEmail('UsEr@ExAmPlE.cOm')
        
        assert str(email1) == str(email2) == str(email3)
        assert email1 == email2 == email3
    
    @pytest.fixture
    def sample_emails(self):
        """Fixture providing sample emails for testing."""
        return {
            'standard': em.StandardEmail(TEST_STANDARD_EMAIL),
            'university': em.UniversityEmail(TEST_UNIVERSITY_EMAIL),
        }
    
    def test_with_sample_emails_fixture(self, sample_emails):
        """Test using fixture with sample emails."""
        assert isinstance(sample_emails['standard'], em.StandardEmail)
        assert isinstance(sample_emails['university'], em.UniversityEmail)
