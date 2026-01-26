---
applyTo: '**/*.{php,yml,yaml,xml}'
description: Standards for testing Yii2 applications with Codeception and PHPUnit in Docker
name: Yii2 Testing Standards
---

# Yii2 Testing Standards

## 1. Environment & Configuration

### Docker-First Approach

- **Execution:** All test commands must be run inside the container.
  - Pattern: `docker-compose exec [service_name] [command]`
  - Example: `docker-compose exec app vendor/bin/codecept run`
- **Database:**
  - Use a separate `test` database container or a `_test` schema.
  - Configure `tests/unit.suite.yml` and `tests/functional.suite.yml` to use the test DB connection.
- **Service Detection:** Always analyze `docker-compose.yaml` to identify the PHP/Application service name before generating commands.

### Frameworks

- **Primary:** **Codeception** (Yii2 Standard). Use for Unit, Functional, and Acceptance tests.
- **Secondary:** **PHPUnit**. Use for isolated unit tests if specifically requested or for pure logic components unrelated to Yii2 application structure.

## 2. Directory Structure (Basic Template)

Follow the standard Yii2 Basic structure:

```text
tests/
├── _data/              # Database dumps and fixtures
├── _output/            # Test artifacts (do not commit)
├── _support/           # Helper classes and Actors
│   ├── Helper/
│   ├── UnitTester.php
│   └── FunctionalTester.php
├── acceptance/         # Browser-based tests
├── api/                # API tests
├── functional/         # Controller/Internal Request tests
├── unit/               # Models/Components tests
├── codeception.yml     # Main configuration
└── docker-compose.yml  # (Optional) Test-specific infrastructure
```

## 3. Test Categories & Templates

### Unit Tests (Models, Components)

Focus on validation, logic, and active record behavior.

```php
<?php
namespace tests\unit\models;

use app\models\User;
use Codeception\Test\Unit;

/**
 * Tests for User Model.
 *
 * @see \app\models\User
 */
class UserTest extends Unit
{
    /**
     * @var \UnitTester
     */
    protected $tester;

    protected function _before()
    {
        // Load fixtures or prepare state
    }

    /**
     * Test validation rules for the user model.
     * Explain the business rule being tested here.
     */
    public function testValidation()
    {
        $user = new User();

        // 1. Test required fields
        $user->username = null;
        $this->assertFalse($user->validate(['username']), 'Username should be required');

        // 2. Test valid state
        $user->username = 'testuser';
        $user->email = 'test@example.com';
        $this->assertTrue($user->validate(), 'User should be valid with correct data');
    }
}
```

### Functional Tests (Controllers)

Focus on request handling, response codes, and basic HTML presence without a browser.

```php
<?php
namespace tests\functional;

use tests\FunctionalTester;

class LoginFormCest
{
    /**
     * @param FunctionalTester $I
     */
    public function _before(FunctionalTester $I)
    {
        $I->amOnPage(['site/login']);
    }

    /**
     * Verify that the login page loads correctly.
     */
    public function openLoginPage(FunctionalTester $I)
    {
        $I->see('Login', 'h1');
        $I->seeElement('form#login-form');
    }

    /**
     * Verify successful login logic.
     */
    public function internalLoginSuccessfully(FunctionalTester $I)
    {
        $I->submitForm('#login-form', [
            'LoginForm[username]' => 'admin',
            'LoginForm[password]' => 'admin',
        ]);
        $I->see('Logout (admin)');
        $I->dontSeeElement('form#login-form');
    }
}
```

## 4. Fixtures & Mock Data

- **Fixtures:** Use Yii2 Fixture framework (`yii\test\ActiveFixture`).
- **Location:** Place fixture classes in `tests/_support/Fixtures` (or `fixtures` folder if configured) and data in `tests/_data`.
- **Usage:** Load fixtures in the `_before()` method or via Codeception Actor methods.

## 5. Best Practices (Senior Tester Persona)

1.  **Readability:** Tests must be readable by a junior developer. Avoid complex metaphysical loops.
2.  **Documentation:**
    - Add PHPDoc to every test method describing _what_ and _why_ it is testing.
    - Comment complex assertions.
3.  **Isolation:** Tests should not depend on each other. Clean up data in `_after()` or rely on transaction rollbacks (Codeception default for DB module).
4.  **Simplicity:**
    - Use `$I->see()` over complex XPath selectors when possible.
    - Use descriptive assertion messages: `$this->assertTrue($condition, 'Error message explaining failure');`.
5.  **Setup Check:** Before running tests, ensure `migrations` are applied to the test database.
