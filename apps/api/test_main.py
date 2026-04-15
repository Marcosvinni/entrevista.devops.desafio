import pytest
from fastapi.testclient import TestClient
from main import app, items_db, audit_log, metrics

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Reset application state between tests."""
    items_db.clear()
    audit_log.clear()
    # Re-seed initial item
    from datetime import datetime
    items_db["1"] = {
        "id": "1",
        "name": "Item de Exemplo",
        "description": "Este é um item de exemplo criado automaticamente",
        "created_at": datetime.now().isoformat(),
        "created_by": "system",
        "category": "default",
        "price": 0.0,
        "active": True
    }
    yield


class TestHealthCheck:
    """Testes para o endpoint de health check."""

    def test_health_check_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_contains_timestamp(self):
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data

    def test_health_check_contains_version(self):
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "2.1.0"

    def test_health_check_contains_environment(self):
        response = client.get("/health")
        data = response.json()
        assert "environment" in data


class TestReadinessCheck:
    """Testes para o endpoint de readiness."""

    def test_readiness_returns_200(self):
        response = client.get("/ready")
        assert response.status_code == 200

    def test_readiness_returns_ready_true(self):
        response = client.get("/ready")
        data = response.json()
        assert data["ready"] is True

    def test_readiness_contains_checks(self):
        response = client.get("/ready")
        data = response.json()
        assert "checks" in data
        assert "database" in data["checks"]
        assert "cache" in data["checks"]


class TestMetrics:
    """Testes para o endpoint de métricas."""

    def test_metrics_returns_200(self):
        response = client.get("/metrics")
        assert response.status_code == 200

    def test_metrics_contains_request_counts(self):
        response = client.get("/metrics")
        data = response.json()
        assert "requests_total" in data
        assert "requests_success" in data
        assert "requests_failed" in data

    def test_metrics_contains_items_count(self):
        response = client.get("/metrics")
        data = response.json()
        assert "items_count" in data


class TestListItemsLegacy:
    """Testes para o endpoint legado de listagem de itens."""

    def test_list_items_returns_200(self):
        response = client.get("/api/items")
        assert response.status_code == 200

    def test_list_items_returns_items_list(self):
        response = client.get("/api/items")
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_list_items_returns_total_count(self):
        response = client.get("/api/items")
        data = response.json()
        assert "total" in data
        assert isinstance(data["total"], int)


class TestListItemsV1:
    """Testes para o endpoint v1 de listagem de itens."""

    def test_list_items_v1_returns_200(self):
        response = client.get("/api/v1/items")
        assert response.status_code == 200

    def test_list_items_v1_supports_pagination(self):
        response = client.get("/api/v1/items?skip=0&limit=10")
        data = response.json()
        assert "skip" in data
        assert "limit" in data
        assert data["skip"] == 0
        assert data["limit"] == 10

    def test_list_items_v1_supports_category_filter(self):
        response = client.get("/api/v1/items?category=default")
        assert response.status_code == 200

    def test_list_items_v1_supports_active_only_filter(self):
        response = client.get("/api/v1/items?active_only=true")
        assert response.status_code == 200


class TestCreateItem:
    """Testes para o endpoint de criação de itens."""

    def test_create_item_returns_201(self):
        payload = {"name": "Test Item", "description": "Test Description"}
        response = client.post("/api/items", json=payload)
        assert response.status_code == 201

    def test_create_item_returns_item_with_id(self):
        payload = {"name": "Test Item 2"}
        response = client.post("/api/items", json=payload)
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Item 2"

    def test_create_item_without_description(self):
        payload = {"name": "Item without description"}
        response = client.post("/api/items", json=payload)
        data = response.json()
        assert data["description"] is None

    def test_create_item_with_description(self):
        payload = {"name": "Item with desc", "description": "My description"}
        response = client.post("/api/items", json=payload)
        data = response.json()
        assert data["description"] == "My description"

    def test_create_item_v1_with_category(self):
        payload = {"name": "Categorized Item", "category": "electronics"}
        response = client.post("/api/v1/items", json=payload)
        data = response.json()
        assert data["category"] == "electronics"

    def test_create_item_v1_with_price(self):
        payload = {"name": "Priced Item", "price": 99.99}
        response = client.post("/api/v1/items", json=payload)
        data = response.json()
        assert data["price"] == 99.99

    def test_create_item_empty_name_fails(self):
        payload = {"name": ""}
        response = client.post("/api/v1/items", json=payload)
        assert response.status_code == 422


class TestGetItem:
    """Testes para o endpoint de busca de item por ID."""

    def test_get_existing_item(self):
        payload = {"name": "Item to Get"}
        create_response = client.post("/api/items", json=payload)
        item_id = create_response.json()["id"]

        response = client.get(f"/api/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["id"] == item_id

    def test_get_nonexistent_item_returns_404(self):
        response = client.get("/api/items/nonexistent-id")
        assert response.status_code == 404

    def test_get_item_v1_endpoint(self):
        payload = {"name": "V1 Item to Get"}
        create_response = client.post("/api/v1/items", json=payload)
        item_id = create_response.json()["id"]

        response = client.get(f"/api/v1/items/{item_id}")
        assert response.status_code == 200


class TestUpdateItem:
    """Testes para o endpoint de atualização de itens."""

    def test_update_item_returns_200(self):
        payload = {"name": "Item to Update"}
        create_response = client.post("/api/v1/items", json=payload)
        item_id = create_response.json()["id"]

        update_payload = {"name": "Updated Name"}
        response = client.put(f"/api/v1/items/{item_id}", json=update_payload)
        assert response.status_code == 200

    def test_update_item_changes_name(self):
        payload = {"name": "Original Name"}
        create_response = client.post("/api/v1/items", json=payload)
        item_id = create_response.json()["id"]

        update_payload = {"name": "New Name"}
        response = client.put(f"/api/v1/items/{item_id}", json=update_payload)
        assert response.json()["name"] == "New Name"

    def test_update_item_sets_updated_at(self):
        payload = {"name": "Item for Update"}
        create_response = client.post("/api/v1/items", json=payload)
        item_id = create_response.json()["id"]

        update_payload = {"description": "Updated description"}
        response = client.put(f"/api/v1/items/{item_id}", json=update_payload)
        assert response.json()["updated_at"] is not None

    def test_update_nonexistent_item_returns_404(self):
        update_payload = {"name": "Doesn't matter"}
        response = client.put("/api/v1/items/nonexistent-id", json=update_payload)
        assert response.status_code == 404

    def test_update_item_active_status(self):
        payload = {"name": "Active Item"}
        create_response = client.post("/api/v1/items", json=payload)
        item_id = create_response.json()["id"]

        update_payload = {"active": False}
        response = client.put(f"/api/v1/items/{item_id}", json=update_payload)
        assert response.json()["active"] is False


class TestDeleteItem:
    """Testes para o endpoint de remoção de itens."""

    def test_delete_existing_item(self):
        payload = {"name": "Item to Delete"}
        create_response = client.post("/api/items", json=payload)
        item_id = create_response.json()["id"]

        response = client.delete(f"/api/items/{item_id}")
        assert response.status_code == 200

    def test_delete_nonexistent_item_returns_404(self):
        response = client.delete("/api/items/nonexistent-id")
        assert response.status_code == 404

    def test_delete_item_v1_returns_id(self):
        payload = {"name": "V1 Item to Delete"}
        create_response = client.post("/api/v1/items", json=payload)
        item_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/items/{item_id}")
        data = response.json()
        assert data["id"] == item_id


class TestAPIKeyAuthentication:
    """Testes para autenticação via API Key."""

    def test_valid_api_key_accepted(self):
        headers = {"X-API-Key": "dev-api-key-12345"}
        response = client.get("/api/v1/items", headers=headers)
        assert response.status_code == 200

    def test_invalid_api_key_rejected(self):
        headers = {"X-API-Key": "invalid-key"}
        response = client.get("/api/v1/items", headers=headers)
        assert response.status_code == 401

    def test_no_api_key_still_works(self):
        # API key is optional for most endpoints
        response = client.get("/api/v1/items")
        assert response.status_code == 200


class TestUserEndpoint:
    """Testes para o endpoint de usuário."""

    def test_get_user_with_valid_key(self):
        headers = {"X-API-Key": "dev-api-key-12345"}
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200

    def test_get_user_returns_user_info(self):
        headers = {"X-API-Key": "dev-api-key-12345"}
        response = client.get("/api/v1/users/me", headers=headers)
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert "role" in data

    def test_get_user_without_key_fails(self):
        response = client.get("/api/v1/users/me")
        assert response.status_code == 422  # Missing required header


class TestDebugEndpoints:
    """Testes para endpoints de debug."""

    def test_debug_config_available_in_debug_mode(self):
        response = client.get("/debug/config")
        assert response.status_code == 200

    def test_debug_audit_available(self):
        response = client.get("/debug/audit")
        assert response.status_code == 200

    def test_debug_audit_returns_entries(self):
        # Make some requests first
        client.get("/health")
        client.get("/metrics")

        response = client.get("/debug/audit")
        data = response.json()
        assert "entries" in data
        assert "total_entries" in data


class TestRequestHeaders:
    """Testes para headers de resposta."""

    def test_response_contains_request_id(self):
        response = client.get("/health")
        assert "X-Request-ID" in response.headers

    def test_response_contains_process_time(self):
        response = client.get("/health")
        assert "X-Process-Time" in response.headers
