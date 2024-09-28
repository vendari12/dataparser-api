import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .utils import normalize_data, reconcile, generate_csv_report
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class CSVReconciliationView(View):
    """
    A view to handle the reconciliation of two CSV files (source and target). This class handles
    file uploads, data normalization, and reconciliation. It also provides reconciliation reports
    in JSON, CSV, or HTML format.
    """

    def post(self, request) -> JsonResponse:
        """
        Handles the POST request to reconcile two CSV files (source and target) and returns the reconciliation report.
        
        Returns:
            JsonResponse or HttpResponse: A JSON response containing the reconciliation report or an error message,
                                          or a CSV/HTML report based on the requested format.
        """
        source_file = request.FILES.get('source')
        target_file = request.FILES.get('target')

        # Error handling for file uploads
        if not source_file or not target_file:
            return JsonResponse({"error": "Both source and target files are required."}, status=400)

        try:
            # Save uploaded files temporarily
            source_path = default_storage.save('source.csv', ContentFile(source_file.read()))
            target_path = default_storage.save('target.csv', ContentFile(target_file.read()))

            # Load CSV files into pandas DataFrames for easier processing
            source_df = pd.read_csv(default_storage.path(source_path))
            target_df = pd.read_csv(default_storage.path(target_path))

            # Normalize data
            source_df = normalize_data(source_df)
            target_df = normalize_data(target_df)

            # Reconcile records
            missing_in_target, missing_in_source, discrepancies = reconcile(source_df, target_df)

            # Generate reconciliation report
            report_format:str = request.GET.get('format', 'json')
            if report_format == 'csv':
                response = generate_csv_report(missing_in_target, missing_in_source, discrepancies)
                return response
            elif report_format == 'html':
                context = {
                    'missing_in_target': missing_in_target,
                    'missing_in_source': missing_in_source,
                    'discrepancies': discrepancies
                }
                return render(request, 'reconcilation_report.html', context)
            else:
                report = {
                    "missing_in_target": missing_in_target.to_dict(orient='records'),
                    "missing_in_source": missing_in_source.to_dict(orient='records'),
                    "discrepancies": discrepancies,
                }
                return JsonResponse(report)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)