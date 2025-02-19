# Devsplug Project Documentation: Refactored and Improved

**Owner:** asbilim  
**Project:** Devsplug  
**Version:** 2.0  
**Last Updated:** 2025-02-16

---

## Table of Contents

- [Devsplug Project Documentation: Refactored and Improved](#devsplug-project-documentation-refactored-and-improved)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Original Architecture and Issues](#2-original-architecture-and-issues)
    - [Overview of the Original System](#overview-of-the-original-system)
    - [Key Problems Identified](#key-problems-identified)
  - [3. Refactoring Objectives](#3-refactoring-objectives)
  - [4. New System Overview](#4-new-system-overview)
    - [4.1 Modern Admin Interface](#41-modern-admin-interface)
    - [4.1 Consolidated Challenge and Submission System](#41-consolidated-challenge-and-submission-system)
    - [4.2 Improved User Management](#42-improved-user-management)
    - [4.3 Enhanced Social Features](#43-enhanced-social-features)
    - [4.1 Challenge Categories and Learning Paths](#41-challenge-categories-and-learning-paths)
    - [4.2 Challenge Attachments](#42-challenge-attachments)
    - [4.3 User Progress Tracking](#43-user-progress-tracking)
    - [4.4 Challenge Subscriptions and Progress Tracking](#44-challenge-subscriptions-and-progress-tracking)
  - [5. API Endpoints and Workflow](#5-api-endpoints-and-workflow)
    - [Authentication Endpoints (unchanged)](#authentication-endpoints-unchanged)
    - [Challenge and Social Endpoints](#challenge-and-social-endpoints)
  - [6. Implementation Details](#6-implementation-details)
    - [6.1 Models](#61-models)
      - [Challenge \& Solution](#challenge--solution)
      - [Social Models](#social-models)
    - [6.2 Views](#62-views)
    - [6.3 Serializers](#63-serializers)
  - [7. Testing and Future Extensions](#7-testing-and-future-extensions)
    - [Testing](#testing)
    - [Future Extensions](#future-extensions)
    - [Test Documentation](#test-documentation)
  - [🔍 Test Coverage](#-test-coverage)
  - [📋 Development Guidelines](#-development-guidelines)
  - [🚦 CI/CD Integration](#-cicd-integration)
  - [📈 Performance Metrics](#-performance-metrics)
  - [🤝 Contributing](#-contributing)
  - [📝 License](#-license)
  - [8. Conclusion](#8-conclusion)
  - [Authentication System Details](#authentication-system-details)
    - [Authentication Flow](#authentication-flow)
    - [API Endpoints](#api-endpoints)
    - [Email Templates](#email-templates)
    - [Security Features](#security-features)
    - [Testing Coverage](#testing-coverage)
    - [Test Examples](#test-examples)
    - [Development Guidelines](#development-guidelines)
    - [Monitoring and Logging](#monitoring-and-logging)
    - [Future Improvements](#future-improvements)
  - [Frontend Integration Guide](#frontend-integration-guide)
    - [Authentication Flow Integration](#authentication-flow-integration)
      - [1. User Registration](#1-user-registration)
      - [2. Account Activation](#2-account-activation)
      - [3. User Login](#3-user-login)
      - [4. Token Refresh](#4-token-refresh)
    - [Social Authentication](#social-authentication)
      - [1. GitHub Authentication](#1-github-authentication)
      - [2. Google Authentication](#2-google-authentication)
      - [3. GitLab Authentication](#3-gitlab-authentication)
    - [User Management](#user-management)
      - [1. Get User Profile](#1-get-user-profile)
      - [2. Update Profile](#2-update-profile)
    - [Social Features](#social-features)
      - [1. Follow User](#1-follow-user)
      - [2. Get Followers/Following](#2-get-followersfollowing)
      - [3. Leaderboard](#3-leaderboard)
    - [Error Handling](#error-handling)
    - [Implementation Examples](#implementation-examples)
      - [React Example](#react-example)
      - [Vue Example](#vue-example)
    - [WebSocket Integration (Future)](#websocket-integration-future)
    - [Rate Limiting](#rate-limiting)
  - [Email Verification System](#email-verification-system)
    - [Email Templates](#email-templates)
    - [Verification Process](#verification-process)
    - [Password Reset](#password-reset)
    - [Security Features](#security-features)
    - [API Endpoints](#api-endpoints)

---

## 1. Introduction

The Devsplug project is designed to encourage continuous coding practice by presenting users with coding challenges, rewarding them with points, and facilitating community engagement. This documentation outlines the comprehensive refactoring and improvements made to the project. The primary goals were to simplify the data model, streamline the user workflow, and enhance social features—all while keeping the original authentication endpoints intact.

---

## 2. Original Architecture and Issues

### Overview of the Original System

- **Multiple Overlapping Models:** Several models (e.g., `ProblemItem`, `Problems`, `ProblemQuiz`) were used to represent various aspects of challenges, resulting in redundancy and confusion.
- **Mixed Challenge and Quiz Workflow:** The original submission process was intertwined with unwanted quiz logic, making solution evaluation and point allocation complex.
- **Scattered Social Features:** Functionality such as comments, likes/dislikes, and follow/unfollow were implemented in a fragmented manner.
- **Complicated User Point System:** Point management and updating user titles were handled in a scattered fashion across the project, leading to maintenance challenges.

### Key Problems Identified

- **Redundancy:** Multiple models serving similar purposes.
- **Complexity:** Over-complicated solution submission and grading logic.
- **Maintenance:** Difficult to extend or modify due to tightly coupled features.

---

## 3. Refactoring Objectives

The refactoring process aimed to:

- **Simplify the Data Model:** Consolidate redundant models into a clean, manageable structure.
- **Streamline the Workflow:** Separate challenge-related functionality from social features without removing any critical capabilities.
- **Enhance User Interaction:** Provide a clear and engaging user journey that seamlessly integrates coding challenges with social interactions.
- **Maintain Core Authentication:** Preserve the existing authentication endpoints so that users encounter no disruption during login, registration, or password management.

---

## 4. New System Overview

### 4.1 Modern Admin Interface

The administrative interface has been completely overhauled using Django Unfold:

- **Enhanced UI/UX:** Modern, responsive interface with improved navigation
- **Advanced Filtering:** Sophisticated filtering and search capabilities
- **Data Visualization:** Better presentation of temporal and relational data
- **Content Management:** Streamlined content editing with TextField

_Key Features:_

- Date hierarchies for temporal navigation
- Preview capabilities for content and files
- Custom list displays with relevant information
- Advanced filtering and search functionality
- Improved model relationships and organization

### 4.1 Consolidated Challenge and Submission System

**Before:**  
Multiple overlapping models and a complex quiz system created unnecessary complexity.

**After:**

- Removed quiz-related functionality entirely
- **Challenge Model:** One unified model defines challenges with clear attributes
- **Solution Model:** A single model now manages all submissions
- **Simplified Content:** Standard TextField for content management
- **Clear Separation:** Distinct legacy and new challenge systems

_Example Workflow:_

- An administrator creates a challenge using the modern admin interface
- Users view available challenges
- Users submit solutions with both code and documentation
- Accepted solutions automatically award points and update the user's rank

### 4.2 Improved User Management

**Before:**  
The user model incorporated a scattered point system and title updating logic.

**After:**

- **Centralized Point Tracking:** The user model now features a clear `add_points` method. This method not only updates the user's score but also adjusts their title based on predefined thresholds.
- **Clean and Maintainable Logic:** The point system and title progression are now encapsulated in a few dedicated methods, making future adjustments easier.

_Key Benefits:_

- Immediate feedback on solution review.
- Transparent progression where users see their title evolve as their score increases.

### 4.3 Enhanced Social Features

The refactoring preserves and enhances all existing social functionalities:

- **Documentation:** Users can now provide detailed explanations via the `documentation` field in the **Solution** model.
- **Comments:** A dedicated **Comment** model supports posting and replying to comments on solutions, fostering richer interactions.
- **Likes/Dislikes:** Separate **Like** and **Dislike** models allow users to express approval or disapproval of submitted solutions.
- **Follow/Unfollow:** A **Follow** model offers users the capability to follow or unfollow others, strengthening community engagement.
- **Challenge Subscriptions:** Users can now subscribe to challenges they're interested in and track their progress.

### 4.4 Challenge Subscriptions and Progress Tracking

The system now includes comprehensive challenge subscription and progress tracking:

- **Challenge Subscriptions**

  - Users can subscribe to challenges they're interested in
  - Track subscription status and dates
  - View all subscribed challenges in their dashboard
  - Unsubscribe when no longer interested

- **Solution Documentation**

  - Each solution can include detailed documentation
  - Users can explain their approach and thought process
  - Documentation helps others learn from solutions
  - Supports knowledge sharing within the community

- **Progress Tracking**
  - Track attempts per challenge
  - Monitor successful vs. total attempts
  - View completion status and dates
  - See last attempt timestamps

### 4.1 Challenge Categories and Learning Paths

The system now supports organized learning paths through categories:

- **Categories**: Challenges are grouped into categories (e.g., "Python Mastery", "Web Development")
- **Prerequisites**: Challenges can have prerequisites to ensure proper learning progression
- **Progress Tracking**: Users can track their progress in each category

#### Category Features

- Unique slug for URL-friendly paths
- Icon support (Font Awesome)
- Order for custom sorting
- Category statistics
  - Total challenges
  - Average difficulty
  - Total solutions submitted

### 4.2 Challenge Attachments

Challenges can now include attachments:

- **File Types**:

  - Templates (`template`)
  - Test Cases (`test_case`)
  - Datasets (`dataset`)
  - Additional Resources

- **Attachment Features**:
  - File upload and storage
  - Description and type categorization
  - Secure access control
  - Preview in admin interface

### 4.3 User Progress Tracking

Enhanced user progress tracking:

- **Overall Progress**:

  - Total challenges completed
  - Total points earned
  - Recent solutions

- **Category Progress**:
  - Completion percentage by category
  - Challenges remaining
  - Category-specific statistics

---

## 5. API Endpoints and Workflow

### Authentication Endpoints (unchanged)

- **User Login/Registration**
- **Token Management**
- **Password Reset and Activation**

### Challenge and Social Endpoints

- **Challenges:** View all challenges, fetch details by slug, etc.
- **Solutions:** Submit a solution, update documentation, retrieve user-specific submissions.
- **Comments:** Create, retrieve, and reply to comments on solutions.
- **Reactions:** Endpoints to add or remove likes/dislikes.
- **Follow System:** Endpoints to follow or unfollow a user.
- **Challenge Management**

```http
# Challenge Management
GET /api/challenges/                    # List all challenges
GET /api/challenges/{slug}/            # Get challenge details
POST /api/challenges/{slug}/subscribe   # Subscribe to a challenge
POST /api/challenges/{slug}/unsubscribe # Unsubscribe from a challenge

# Subscriptions
GET /api/subscriptions/                # List user's subscribed challenges

# Solutions
POST /api/challenges/{slug}/solutions/  # Submit a solution with documentation
GET /api/challenges/{slug}/solutions/   # List solutions for a challenge
```

### Challenge Response Format

```json
{
  "id": 1,
  "title": "Python Variables",
  "slug": "python-variables",
  "description": "Learn Python variables",
  "difficulty": "easy",
  "points": 10,
  "category": {
    "name": "Python Mastery",
    "slug": "python-mastery",
    "icon": "fa-python"
  },
  "tags": ["python", "basics"],
  "attachments": [
    {
      "title": "test_template.py",
      "file": "/media/attachments/test_template.py",
      "description": "Template for testing",
      "file_type": "template"
    }
  ],
  "prerequisites": [],
  "estimated_time": 30,
  "completion_rate": 75.5,
  "user_status": {
    "status": "completed",
    "submitted_at": "2024-02-18T12:00:00Z"
  }
}
```

### Progress Response Format

```json
{
  "total_challenges": 50,
  "completed_challenges": 25,
  "total_points": 500,
  "completion_by_category": {
    "Python Mastery": {
      "total": 20,
      "completed": 15,
      "percentage": 75.0
    },
    "Web Development": {
      "total": 30,
      "completed": 10,
      "percentage": 33.3
    }
  },
  "recent_solutions": [
    {
      "challenge": {
        "title": "Python Decorators",
        "slug": "python-decorators",
        "difficulty": "hard"
      },
      "status": "accepted",
      "submitted_at": "2024-02-18T14:30:00Z"
    }
  ]
}
```

### Subscription Response Format

```json
{
  "id": 1,
  "challenge": {
    "title": "Python Variables",
    "slug": "python-variables",
    "difficulty": "easy",
    "points": 10,
    "category": {
      "name": "Python Mastery",
      "slug": "python-mastery"
    }
  },
  "is_subscribed": true,
  "subscribed_at": "2024-02-19T12:00:00Z",
  "last_attempted_at": "2024-02-19T14:30:00Z",
  "completed": true,
  "completed_at": "2024-02-19T14:30:00Z",
  "attempts": 3,
  "successful_attempts": 1
}
```

### Solution Response Format

```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "johndoe",
    "profile": "https://example.com/profile.jpg",
    "title": "Developer"
  },
  "challenge": 1,
  "code": "def solution():\n    return 'Hello World'",
  "documentation": "This solution uses a simple function that returns a greeting...",
  "language": "python",
  "status": "accepted",
  "created_at": "2024-02-19T12:00:00Z",
  "is_private": false
}
```

---

## 6. Implementation Details

### 6.1 Models

#### Challenge & Solution

- **Challenge Model:** Defines challenge properties and manages attachments and tags.
- **Solution Model:** Manages solution submissions and includes a documentation field. When a solution is accepted, points are auto-awarded.
- **UserChallenge Model:** Tracks user subscriptions to challenges and maintains progress information.

_Key Features:_

- Solution documentation support
- Challenge subscription tracking
- Progress monitoring
- Multiple attempts tracking

_Refer to:_ `challenges/models.py`

#### Social Models

- **Comment Model:** For user comments and nested replies.
- **Like / Dislike Models:** For user reactions to solutions.
- **Follow Model:** Manages follower relationships between users.

_Refer to:_ `challenges/models.py` and `authentication/models.py` (for Follow).

### 6.2 Views

- **ChallengeViewSet:** Handles retrieving challenges and solution submissions.
- **SolutionViewSet:** Manages user submissions.
- **FollowViewSet:** Manages follow/unfollow requests.

_Refer to:_ `challenges/views.py` and `authentication/views.py`

### 6.3 Serializers

Serializers are adjusted to match the refactored models:

- **ChallengeSerializer**
- **SolutionSerializer**
- **CommentSerializer**
- **LikeSerializer / DislikeSerializer**
- **FollowSerializer**

_Refer to:_ `challenges/serializer.py` and `authentication/serializer.py`

---

## 7. Testing and Future Extensions

### Testing

- **Unit Testing:** Validate models, views, and serializers.
- **Integration Testing:** Test end-to-end workflows (challenge submission, point awarding, social interactions).
- **API Testing:** Ensure all endpoints respond as expected.

### Future Extensions

- **Automated Code Evaluation:** Integrate automated testing of submitted code.
- **Real-Time Notifications:** Implement WebSocket support for live updates.
- **Enhanced User Feeds:** Create personalized feeds based on follow relationships.
- **Advanced Commenting:** Introduce threaded discussions and moderation tools.

### Test Documentation

Each test includes:

- Clear description of what's being tested
- Test setup information
- Input data used
- Expected responses
- Actual results
- Error messages (if any)

## 🔍 Test Coverage

The test suite covers:

- Model validations
- API endpoints
- Business logic
- Edge cases
- Error handling
- Authorization rules

## 📋 Development Guidelines

1. **Writing Tests**

   - Include docstrings explaining test purpose
   - Set up clear test data
   - Track responses using `self.current_test_response`
   - Test both success and failure cases

2. **Test Structure**

   ```python
   def test_example(self):
       """Clear description of what this test verifies"""
       # Setup
       self.test_data = {...}

       # Execute
       response = self.client.post(url, self.test_data)

       # Assert
       self.assertEqual(response.status_code, expected_status)

       # Track for reporting
       self.current_test_response = {
           'status_code': response.status_code,
           'data': response.data
       }
   ```

## 🚦 CI/CD Integration

The test suite is integrated with:

- GitHub Actions
- Pre-commit hooks
- Deployment pipelines

## 📈 Performance Metrics

- Average test execution time: ~1.5s
- Test coverage: >90%
- Zero flaky tests

## 🤝 Contributing

1. Write tests for new features
2. Ensure all tests pass
3. Follow the test documentation format
4. Update README.md as needed

## 📝 License

MIT License - see LICENSE file for details

---

## 8. Conclusion

This refactored architecture of Devsplug:

- **Simplifies and consolidates the data models,** reducing redundancy and improving maintainability.
- **Streamlines the challenge and solution submission process,** ensuring a clear, user-friendly workflow.
- **Enhances social functionality,** preserving vital features such as commenting, liking/disliking, and following.
- **Improves user management,** with a robust and transparent point and title progression system.

The refactoring effort ensures that Devsplug remains a robust platform for regular coding challenges, facilitating community engagement and continuous improvement.

---

_Documentation prepared by asbilim_

## Authentication System Details

### Authentication Flow

1. **Registration Flow**

   ```
   User Registration -> Email Verification -> Account Activation
   ```

   - User provides username, email, and password
   - System sends verification code via email
   - User activates account using the code

2. **Password Reset Flow**

   ```
   Request Reset -> Verify Code -> Change Password
   ```

   - User requests password reset with email
   - System sends verification code
   - User verifies code
   - User sets new password

3. **Profile Management**
   - Update profile information (including image)
   - Change password while logged in
   - Update motivation/bio
   - View and manage followers

### API Endpoints

#### Authentication

```
POST /api/user/create           # Register new user
POST /api/user/activate         # Activate account with code
POST /api/user/password/apply   # Request password reset
POST /api/user/password/verify  # Verify reset code
POST /api/user/password/change  # Change password with code
POST /api/token/                # Get JWT token
POST /api/token/refresh/        # Refresh JWT token
```

#### Profile Management

```
PATCH /api/user/update/<id>     # Update profile
POST /api/user/motivation-edit  # Update motivation/bio
GET /api/user/me                # Get current user info
```

### Email Templates

1. **Registration Verification**

   ```
   Subject: Devsplug verification code
   Content: Hello {username} this is your Devsplug verification code: {code}
   ```

2. **Password Reset**
   ```
   Subject: Devsplug password verification code
   Content: Hello {username} this is your Devsplug verification code: {code}
   ```

### Security Features

- JWT Authentication with refresh tokens
- Email verification for registration
- Two-step password reset process
- Secure password hashing
- Rate limiting on sensitive endpoints
- Permission-based access control

### Testing Coverage

The authentication system includes comprehensive tests for:

1. **User Registration**

   - Successful registration
   - Duplicate username/email handling
   - Email verification
   - Account activation

2. **Password Management**

   - Password reset flow
   - Password change while logged in
   - Invalid code handling
   - Email verification

3. **Profile Updates**

   - Profile image upload
   - Information updates
   - Validation checks
   - Permission verification

4. **Email System**
   - Email sending verification
   - Template rendering
   - Error handling
   - Content verification

### Test Examples

```python
def test_registration_and_activation_flow(self):
    """
    Tests the complete registration and activation process:
    1. Register user
    2. Verify inactive status
    3. Check verification code
    4. Verify email sending
    5. Activate account
    6. Confirm active status
    """
    # Implementation details...

def test_password_reset_flow(self):
    """
    Tests the complete password reset process:
    1. Request reset
    2. Verify code generation
    3. Check email
    4. Verify code
    5. Change password
    6. Verify new login
    """
    # Implementation details...

def test_profile_update(self):
    """
    Tests profile update functionality:
    1. Update basic info
    2. Upload profile image
    3. Update motivation
    4. Verify changes
    """
    # Implementation details...
```

### Development Guidelines

1. **Email Configuration**

   - Development: Uses console backend
   - Testing: Uses console backend with logging
   - Production: Uses SMTP with proper credentials

2. **File Upload Handling**

   - Supports image uploads for profiles
   - Validates file types and sizes
   - Uses secure storage backend

3. **Error Handling**

   - Proper status codes for different scenarios
   - Descriptive error messages
   - Consistent response format

4. **Testing Requirements**
   - All new features must include tests
   - Email sending must be verified
   - File upload handling must be tested
   - Error scenarios must be covered

### Monitoring and Logging

The system includes comprehensive logging for:

- Email sending attempts
- Failed login attempts
- Password reset requests
- Profile update activities

### Future Improvements

1. **Enhanced Security**

   - Add 2FA support
   - Implement OAuth providers
   - Add session management

2. **User Experience**

   - Real-time email verification
   - Enhanced profile customization
   - Social media integration

3. **Administration**
   - Enhanced user management tools
   - Audit logging
   - Analytics dashboard

## Frontend Integration Guide

### Authentication Flow Integration

#### 1. User Registration

**Endpoint:** `POST /api/user/create`

**Request:**

```json
{
  "username": "testuser",
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "status": "success",
  "content": "User created, verify your email to activate your account"
}
```

#### 2. Account Activation

**Endpoint:** `POST /api/user/activate`

**Request:**

```json
{
  "code": "123456789",
  "email": "user@example.com"
}
```

**Response:**

```json
{
  "status": "success",
  "content": "Account activated successfully"
}
```

#### 3. User Login

**Endpoint:** `POST /api/token/`

**Request:**

```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 4. Token Refresh

**Endpoint:** `POST /api/token/refresh/`

**Request:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Social Authentication

#### 1. GitHub Authentication

**Endpoint:** `POST /auth/github/`

**Request:**

```json
{
  "access_token": "github_oauth_token"
}
```

**Response:**

```json
{
  "access_token": "jwt_token",
  "refresh_token": "jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "githubuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### 2. Google Authentication

**Endpoint:** `POST /auth/google/`

**Request:**

```json
{
  "access_token": "google_oauth_token",
  "code": "google_auth_code" // Optional, for authorization code flow
}
```

**Response:**

```json
{
  "access_token": "jwt_token",
  "refresh_token": "jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "googleuser",
    "email": "user@gmail.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### 3. GitLab Authentication

**Endpoint:** `POST /auth/gitlab/`

**Request:**

```json
{
  "access_token": "gitlab_oauth_token"
}
```

**Response:**

```json
{
  "access_token": "jwt_token",
  "refresh_token": "jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "gitlabuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```
