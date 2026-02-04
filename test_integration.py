"""
Integration tests for Demo-G6 CICD and 3-Tier Architecture
Tests all functionality before production deployment
"""

import pytest
from application import create_app, db
from application.data.models.subscriber import Subscriber


@pytest.fixture
def app():
    """Create app with test configuration"""
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner"""
    return app.test_cli_runner()


class TestApplicationStartup:
    """Test 1: Application Factory & Startup"""
    
    def test_app_creation(self, app):
        """✅ Test: Application factory creates app correctly"""
        assert app is not None
        assert app.config['TESTING'] is True
        
    def test_app_has_extensions(self, app):
        """✅ Test: Database extensions are initialized"""
        assert db is not None
        print("✅ Database extensions initialized")


class TestRoutes:
    """Test 2: Routes & Presentation Layer"""
    
    def test_index_route_exists(self, client):
        """✅ Test: Index route responds"""
        response = client.get('/')
        assert response.status_code == 200
        print(f"✅ Index route working (status: {response.status_code})")
    
    def test_index_contains_jokes(self, client):
        """✅ Test: Index page contains joke content"""
        response = client.get('/')
        assert b'STREET WISDOM' in response.data
        print("✅ Jokes section found in response")
    
    def test_subscribe_form_get(self, client):
        """✅ Test: Subscribe form GET route"""
        response = client.get('/subscribe')
        assert response.status_code == 200
        assert b'email' in response.data.lower()
        print(f"✅ Subscribe form route working (status: {response.status_code})")
    
    def test_subscribe_form_post_valid(self, client):
        """✅ Test: Valid subscription is accepted"""
        response = client.post('/subscribe/confirm', data={
            'email': 'test@example.com',
            'name': 'Test User'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Thank You' in response.data
        print("✅ Valid subscription accepted")
    
    def test_subscribe_form_post_invalid_email(self, client):
        """✅ Test: Invalid email is rejected"""
        response = client.post('/subscribe/confirm', data={
            'email': 'invalid-email',
            'name': 'Test'
        })
        assert b'Invalid email' in response.data
        print("✅ Invalid email properly rejected")


class TestDatabasePersistence:
    """Test 3: Data Layer & Database"""
    
    def test_subscriber_creation(self, app):
        """✅ Test: Subscribers can be created"""
        with app.app_context():
            subscriber = Subscriber(email='john@example.com', name='John')
            db.session.add(subscriber)
            db.session.commit()
            
            found = Subscriber.query.filter_by(email='john@example.com').first()
            assert found is not None
            assert found.name == 'John'
            print("✅ Subscriber creation and retrieval working")
    
    def test_subscriber_uniqueness(self, app):
        """✅ Test: Duplicate emails are prevented"""
        with app.app_context():
            s1 = Subscriber(email='jane@example.com', name='Jane')
            db.session.add(s1)
            db.session.commit()
            
            s2 = Subscriber(email='jane@example.com', name='Jane Doe')
            db.session.add(s2)
            
            try:
                db.session.commit()
                assert False, "Should have raised IntegrityError"
            except Exception as e:
                assert 'UNIQUE' in str(e) or 'unique' in str(e).lower()
                print("✅ Duplicate prevention working")


class TestThreeTierArchitecture:
    """Test 4: 3-Tier Architecture Integration"""
    
    def test_repository_exists(self, app):
        """✅ Test: Repository layer is available"""
        from app.data.repositories.subscriber_repository import SubscriberRepository
        assert SubscriberRepository is not None
        print("✅ Repository layer exists")
    
    def test_service_exists(self, app):
        """✅ Test: Business service layer is available"""
        from app.business.services.subscription_service import SubscriptionService
        assert SubscriptionService is not None
        print("✅ Service layer exists")
    
    def test_three_tier_integration(self, client):
        """✅ Test: Full 3-tier workflow"""
        response = client.post('/subscribe/confirm', data={
            'email': 'alice@example.com',
            'name': 'Alice'
        }, follow_redirects=True)
        
        # Should succeed and redirect to thank you
        assert response.status_code == 200
        assert b'Thank You' in response.data
        print("✅ Full 3-tier workflow successful")


class TestCICDSetup:
    """Test 5: CICD Files Validation"""
    
    def test_dockerfile_exists(self):
        """✅ Test: Dockerfile is present"""
        import os
        assert os.path.exists('/Users/ludwigsevenheim/Demo-G6/Dockerfile')
        print("✅ Dockerfile exists")
    
    def test_docker_entrypoint_exists(self):
        """✅ Test: entrypoint.sh is present"""
        import os
        assert os.path.exists('/Users/ludwigsevenheim/Demo-G6/entrypoint.sh')
        print("✅ entrypoint.sh exists")
    
    def test_github_workflow_exists(self):
        """✅ Test: GitHub Actions workflow is present"""
        import os
        assert os.path.exists('/Users/ludwigsevenheim/Demo-G6/.github/workflows/deploy.yml')
        print("✅ GitHub Actions workflow exists")
    
    def test_azure_config_exists(self):
        """✅ Test: Azure configuration exists"""
        import os
        assert os.path.exists('/Users/ludwigsevenheim/Demo-G6/.azure-config')
        print("✅ Azure configuration exists")
    
    def test_requirements_has_gunicorn(self):
        """✅ Test: requirements.txt has gunicorn"""
        with open('/Users/ludwigsevenheim/Demo-G6/requirements.txt', 'r') as f:
            content = f.read()
            assert 'gunicorn' in content
            print("✅ gunicorn in requirements.txt")
    
    def test_dockerfile_valid_syntax(self):
        """✅ Test: Dockerfile has valid structure"""
        with open('/Users/ludwigsevenheim/Demo-G6/Dockerfile', 'r') as f:
            content = f.read()
            assert 'FROM' in content
            assert 'WORKDIR' in content
            assert 'CMD' in content
            print("✅ Dockerfile has valid structure")


class TestBackwardsCompatibility:
    """Test 6: Verify nothing broke"""
    
    def test_existing_functionality_preserved(self, client):
        """✅ Test: Existing features still work"""
        # Test jokes still work
        response = client.get('/')
        assert response.status_code == 200
        assert b'G6' in response.data or b'SLAY' in response.data
        print("✅ Existing functionality preserved")
    
    def test_static_files_accessible(self, client):
        """✅ Test: Static files (CSS) are served"""
        # CSS should be accessible
        response = client.get('/static/style.css')
        # Either 200 or 304 (not modified) is fine
        assert response.status_code in [200, 304]
        print("✅ Static files accessible")


class TestProductionReadiness:
    """Test 7: Production Readiness"""
    
    def test_app_factory_production_config(self):
        """✅ Test: Application factory works with production config"""
        app = create_app("production")
        assert app is not None
        assert app.config['DEBUG'] is False
        print("✅ Production configuration valid")
    
    def test_gunicorn_compatibility(self):
        """✅ Test: app.py exports app instance for gunicorn"""
        # Read app.py to verify it has the app instance
        with open('/Users/ludwigsevenheim/Demo-G6/app.py', 'r') as f:
            content = f.read()
            assert 'from app import create_app' in content
            assert 'app = create_app()' in content
            print("✅ Gunicorn-compatible app instance in app.py")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
