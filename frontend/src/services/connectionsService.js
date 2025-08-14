import { api } from './api';

export const connectionsService = {
  // Student sends a code (alias endpoint)
  sendRequestViaCode({ invitation_code, relationship, message }) {
    return api.post('/requests/request', { invitation_code, relationship, message })
      .then(r => r.data);
  },

  // My outbound pending requests
  getMyPendingRequests() {
    return api.get('/requests/pending-requests').then(r => {
      const d = r.data
      return Array.isArray(d?.requests) ? d.requests : (Array.isArray(d) ? d : [])
    });
  },

  // Approver/owner pending (family head / teacher)
  getIncomingPending() {
    return api.get('/requests/pending').then(r => r.data);
  },

  // Approve/Reject (unified)
  handleRequest(requestId, action) {
    return api.patch(`/requests/${requestId}/handle`, { action }).then(r => r.data);
  },

  // Activity + Stats + Connections list
  getActivity() {
    return api.get('/connections/activity').then(r => r.data);
  },
  getStats() {
    return api.get('/connections/stats').then(r => r.data);
  },
  listConnections(type) { // type?: teacher_student | parent_student | family
    return api.get('/connections/', { params: { type } }).then(r => {
      const d = r.data
      if (Array.isArray(d)) return d
      if (Array.isArray(d?.connections)) return d.connections
      if (Array.isArray(d?.items)) return d.items
      return []
    });
  },
};
