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

_Example Workflow:_

1. **User Browses Challenges:**  
   The user fetches a list of challenges.
2. **User Submits a Solution:**  
   With both code and documentation.
3. **Solution Review:**  
   An admin or automated evaluation marks the solution as accepted or rejected.
4. **Points and Title Update:**  
   If accepted, points are awarded and the user's title is updated.
5. **Social Interaction:**  
   Other users can comment on, like/dislike, or follow contributors to engage with the community.

---

## 6. Implementation Details

### 6.1 Models

#### Challenge & Solution

- **Challenge Model:** Defines challenge properties and manages attachments and tags.
- **Solution Model:** Manages solution submissions and includes a documentation field. When a solution is accepted, points are auto-awarded.

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

### User Management

#### 1. Get User Profile

**Endpoint:** `GET /api/user/me`

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response:**

```json
{
  "id": 1,
  "username": "testuser",
  "email": "user@example.com",
  "motivation": "Love coding!",
  "score": 500,
  "profile": "https://example.com/profile.jpg",
  "title": "Novice"
}
```

#### 2. Update Profile

**Endpoint:** `PATCH /api/user/update/<user_id>`

**Headers:**

```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request:**

```json
{
    "username": "newusername",
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile": <file>,
    "motivation": "New motivation text"
}
```

**Response:**

```json
{
  "id": 1,
  "username": "newusername",
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile": "https://example.com/new-profile.jpg",
  "motivation": "New motivation text"
}
```

### Social Features

#### 1. Follow User

**Endpoint:** `POST /api/follows/`

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request:**

```json
{
  "following": 2 // User ID to follow
}
```

**Response:**

```json
{
  "id": 1,
  "following": 2,
  "created_at": "2025-02-17T00:28:19.148609Z"
}
```

#### 2. Get Followers/Following

**Endpoint:** `GET /api/follows/`

**Headers:**

```
Authorization: Bearer <access_token>
```

**Response:**

```json
[
  {
    "id": 1,
    "following": {
      "id": 2,
      "username": "user2",
      "profile": "https://example.com/profile2.jpg"
    },
    "created_at": "2025-02-17T00:28:19.148609Z"
  }
]
```

#### 3. Leaderboard

**Endpoint:** `GET /api/leaderboard/`

**Response:**

```json
[
  {
    "id": 1,
    "username": "topuser",
    "score": 1500,
    "profile": "https://example.com/profile.jpg",
    "title": "Developer",
    "motivation": "Coding is life!"
  }
]
```

### Error Handling

All endpoints return appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

Error responses include detailed messages:

```json
{
  "error": "Detailed error message",
  "status": "error"
}
```

### Implementation Examples

#### React Example

```javascript
// Authentication Service
const authService = {
  async login(username, password) {
    const response = await fetch("/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) throw new Error("Login failed");

    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    return data;
  },

  async googleLogin(accessToken) {
    const response = await fetch("/auth/google/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ access_token: accessToken }),
    });

    if (!response.ok) throw new Error("Google login failed");

    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    return data;
  },
};

// Protected API Service
const apiService = {
  async getUserProfile() {
    const response = await fetch("/api/user/me", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

    if (!response.ok) throw new Error("Failed to fetch profile");

    return response.json();
  },
};
```

#### Vue Example

```javascript
// Auth Store (Pinia)
export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    tokens: {
      access: null,
      refresh: null,
    },
  }),

  actions: {
    async login(username, password) {
      try {
        const response = await fetch("/api/token/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        this.tokens = {
          access: data.access_token,
          refresh: data.refresh_token,
        };

        await this.fetchUser();
      } catch (error) {
        console.error("Login failed:", error);
        throw error;
      }
    },

    async fetchUser() {
      try {
        const response = await fetch("/api/user/me", {
          headers: {
            Authorization: `Bearer ${this.tokens.access}`,
          },
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        this.user = data;
      } catch (error) {
        console.error("Failed to fetch user:", error);
        throw error;
      }
    },
  },
});
```

### WebSocket Integration (Future)

For real-time features like notifications, the system will support WebSocket connections:

```javascript
const socket = new WebSocket("ws://api.example.com/ws/notifications/");

socket.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  // Handle notification
};
```

### Rate Limiting

The API implements rate limiting to prevent abuse. Limits are:

- Authentication endpoints: 5 requests per minute
- Profile updates: 10 requests per minute
- Social actions: 30 requests per minute

When rate limited, the API returns:

```json
{
  "error": "Rate limit exceeded",
  "retry_after": 30
}
```
