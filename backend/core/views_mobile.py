from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class OfflineCacheManifestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Placeholder: Return manifest for offline caching
        data = {"manifest": {"endpoints": [
            "/api/dashboard/student/",
            "/api/dashboard/lecturer/",
            "/api/dashboard/registrar/",
            "/api/dashboard/finance/",
            "/api/dashboard/it-admin/",
            "/api/dashboard/hod/",
            "/api/report/academic/",
            "/api/report/financial/",
            "/api/report/departmental/",
            "/api/report/compliance/",
            "/api/report/analytics/",
            "/api/notifications/",
            "/api/ai/academic-insights/",
            "/api/ai/performance-prediction/",
            "/api/ai/financial-trends/",
            "/api/ai/threat-detection/",
            "/api/integration/payment-gateway/",
            "/api/integration/lms/",
            "/api/integration/cloud-storage/",
            "/api/integration/hr-payroll/"
        ]}}
        return Response(data)
