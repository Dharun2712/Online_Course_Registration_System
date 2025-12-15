/**
 * API Client for CourseHub Platform
 * Handles all API requests with authentication
 */

const API_BASE_URL = 'http://localhost:5000/api';

class APIClient {
    constructor() {
        // Backwards-compatible: accept older keys `token`/`user` and new keys `auth_token`/`user_data`
        this.token = localStorage.getItem('auth_token') || localStorage.getItem('token');
        const rawUser = localStorage.getItem('user_data') || localStorage.getItem('user') || 'null';
        try {
            this.user = JSON.parse(rawUser);
        } catch (e) {
            this.user = null;
        }
    }

    // Set auth token
    setToken(token) {
        this.token = token;
        // Write to both keys for compatibility with different pages
        localStorage.setItem('auth_token', token);
        localStorage.setItem('token', token);
    }

    // Get auth token
    getToken() {
        return this.token || localStorage.getItem('auth_token') || localStorage.getItem('token');
    }

    // Set user data
    setUser(user) {
        this.user = user;
        // Store under both keys for pages that expect either
        const serialized = JSON.stringify(user);
        localStorage.setItem('user_data', serialized);
        localStorage.setItem('user', serialized);
    }

    // Get user data
    getUser() {
        if (this.user) return this.user;
        const raw = localStorage.getItem('user_data') || localStorage.getItem('user') || 'null';
        try {
            return JSON.parse(raw);
        } catch (e) {
            return null;
        }
    }

    // Clear auth data
    logout() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
        this.token = null;
        this.user = null;
        window.location.href = '/login';
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.getToken();
    }

    // Make API request
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // Add auth token if available
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                // Handle auth errors
                if (response.status === 401) {
                    this.logout();
                }
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // Auth endpoints
    async register(name, email, password, role = 'student') {
        const data = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password, role })
        });

        if (data.success) {
            this.setToken(data.token);
        }

        return data;
    }

    async login(email, password) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        if (data.success) {
            this.setToken(data.token);
            this.setUser(data.user);
        }

        return data;
    }

    async getProfile() {
        return await this.request('/auth/profile');
    }

    async updateProfile(updates) {
        return await this.request('/auth/profile', {
            method: 'PUT',
            body: JSON.stringify(updates)
        });
    }

    // Student endpoints
    async browseCourses(page = 1, search = '') {
        const query = new URLSearchParams({ page, search });
        return await this.request(`/student/courses?${query}`);
    }

    async getCourseDetails(courseId) {
        return await this.request(`/student/courses/${courseId}`);
    }

    async enrollInCourse(courseId, paymentId = null) {
        return await this.request('/student/enroll', {
            method: 'POST',
            body: JSON.stringify({ course_id: courseId, payment_id: paymentId })
        });
    }

    async getMyCourses(status = null) {
        const query = status ? `?status=${status}` : '';
        return await this.request(`/student/my-courses${query}`);
    }

    async updateProgress(courseId, progressPercent) {
        return await this.request(`/student/progress/${courseId}`, {
            method: 'POST',
            body: JSON.stringify({ progress_percent: progressPercent })
        });
    }

    async chatbot(message, context = null) {
        return await this.request('/student/chatbot', {
            method: 'POST',
            body: JSON.stringify({ message, context })
        });
    }

    async getRecommendations(interests = [], skillLevel = 'beginner') {
        const query = new URLSearchParams();
        interests.forEach(i => query.append('interests', i));
        query.append('skill_level', skillLevel);
        return await this.request(`/student/recommendations?${query}`);
    }

    // Instructor endpoints
    async getInstructorCourses() {
        return await this.request('/instructor/courses');
    }

    async createCourse(courseData) {
        return await this.request('/instructor/courses', {
            method: 'POST',
            body: JSON.stringify(courseData)
        });
    }

    async updateCourse(courseId, updates) {
        return await this.request(`/instructor/courses/${courseId}`, {
            method: 'PUT',
            body: JSON.stringify(updates)
        });
    }

    async publishCourse(courseId) {
        return await this.request(`/instructor/courses/${courseId}/publish`, {
            method: 'POST'
        });
    }

    async addCourseMaterial(courseId, materialData) {
        return await this.request(`/instructor/courses/${courseId}/materials`, {
            method: 'POST',
            body: JSON.stringify(materialData)
        });
    }

    async getCourseStudents(courseId) {
        return await this.request(`/instructor/courses/${courseId}/students`);
    }

    async getInstructorStats() {
        return await this.request('/instructor/statistics');
    }

    // Payment endpoints
    async processDemoPayment(courseId) {
        return await this.request('/payment/demo', {
            method: 'POST',
            body: JSON.stringify({ course_id: courseId })
        });
    }

    async getMyPayments() {
        return await this.request('/payment/my-payments');
    }

    async verifyPayment(courseId) {
        return await this.request(`/payment/verify/${courseId}`);
    }

    // Admin endpoints
    async getAllUsers(role = null, page = 1) {
        const query = new URLSearchParams({ page });
        if (role) query.append('role', role);
        return await this.request(`/admin/users?${query}`);
    }

    async getPendingCourses() {
        return await this.request('/admin/courses/pending');
    }

    async approveCourse(courseId) {
        return await this.request(`/admin/courses/${courseId}/approve`, {
            method: 'POST'
        });
    }

    async rejectCourse(courseId, reason) {
        return await this.request(`/admin/courses/${courseId}/reject`, {
            method: 'POST',
            body: JSON.stringify({ reason })
        });
    }

    async getPlatformStats() {
        return await this.request('/admin/statistics');
    }
}

// Create global API instance
const api = new APIClient();

// Helper functions
function showNotification(message, type = 'info') {
    // Simple notification (can be enhanced with a toast library)
    alert(message);
}

function requireAuth() {
    if (!api.isAuthenticated()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

function checkRole(requiredRole) {
    const user = api.getUser();
    if (!user || !user.role || String(user.role).toLowerCase() !== String(requiredRole).toLowerCase()) {
        showNotification('Unauthorized access', 'error');
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Export for use in HTML files
window.api = api;
window.requireAuth = requireAuth;
window.checkRole = checkRole;
window.showNotification = showNotification;
