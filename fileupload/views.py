import pandas as pd
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import UploadFileForm

def handle_uploaded_file(file):
    # Read Excel file into a DataFrame
    df = pd.read_excel(file)
    
    # Generate summary report
    summary = df.groupby('Cust State').agg({'DPD': 'mean'}).reset_index()
    summary_text = summary.to_string(index=False)
    return summary_text

def file_upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            summary_text = handle_uploaded_file(file)
            
            # Send summary email
            send_mail(
                subject=f"Python Assignment - Ravikishan Gupta",
                message=summary_text,
                from_email='061002kishan@gmail.com',
                recipient_list=['2303340ln8ravikishan@viva-technology.org'],
            )
            return render(request, 'success.html', {'summary': summary_text})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
