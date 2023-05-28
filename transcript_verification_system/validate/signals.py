from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.files import File
from .models import Transcript, SubjectInTranscript

from pathlib import Path
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from fpdf import FPDF
import hashlib
import os

class ValidTranscript(FPDF):

    # Header of the generated PDF
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(50, 10, 'Educational Institute Corp', 1, 0, 'C')

    # Footer of the generated PDF
    def footer(self):
        self.set_y(-20)
        self.set_x(80)

        self.set_font('Arial', 'B', 10)

        self.cell(50, 10, 'Signed by Institute Corp', 1, 1, 'C')

# Generate the PDF
def create_pdf(obj):
    pdf = ValidTranscript()
    pdf.add_page()

    # Add transcript id
    pdf.set_x(-60)
    pdf.cell(50, 10, f'Transcript ID: {obj.id}', 1, 1, 'C')

    subjects = obj.subjects.through.objects.filter(transcript_id=obj.id)

    pdf.cell(140, 10, ln=1)
    pdf.cell(50, 10, f'Student Name:', 1, 0, 'C')
    pdf.cell(140, 10, f'Adam Warlock', 1, 1, 'C')

    pdf.cell(50, 10, f'Student ID:', 1, 0, 'C')
    pdf.cell(140, 10, f'1', 1, 1, 'C')

    pdf.cell(140, 10, ln=1)

    pdf.cell(40, 10, "Subject Code", 1, 0, 'C')
    pdf.cell(110, 10, "Subjects", 1, 0, 'C')
    pdf.cell(20, 10, "Marks", 1, 0, 'C')
    pdf.cell(20, 10, "Grade", 1, 1, 'C')

    for subject in subjects:
        pdf.cell(40, 10, f'{subject.subject.id}', 1, 0, 'C')
        pdf.cell(110, 10, f'{subject.subject.name}', 1, 0, 'C')
        pdf.cell(20, 10, f'{subject.marks}', 1, 0, 'C')
        pdf.cell(20, 10, f'{subject.grade}', 1, 1, 'C')

    temporary_path = f"{settings.MEDIA_ROOT}{obj.id}.pdf"

    pdf.output(temporary_path)

    # Sign the PDF here before exit
    pdf_signer  =   signers.SimpleSigner.load(
                        f'{settings.MEDIA_ROOT}keys/private_key.pem',
                        f'{settings.MEDIA_ROOT}keys/certificate/company.crt'
                    )

    with open(temporary_path, 'rb+') as pdf:
        sign    =   IncrementalPdfFileWriter(pdf)
        out     =   signers.PdfSigner(
                        signers.PdfSignatureMetadata(field_name="Signature"),
                        signer=pdf_signer,
                    ).sign_pdf(sign)

    # Generate SHA256 hash
    with open(temporary_path, 'rb+') as signed:
        signed.write(out.getvalue())
        signature    =   hashlib.sha256(out.getvalue()).hexdigest()


    # Return the temporary obj
    return Path(temporary_path), signature

@receiver(post_save, sender=SubjectInTranscript)
def create_pdf_after_save(sender, instance, **kwargs):
    transcript  =   Transcript.objects.get(id=instance.transcript_id)

    pdf_location, signature    =   create_pdf(transcript)

    file            =   pdf_location.open(mode="rb")

    old_file        =   Path(f'{settings.MEDIA_ROOT}transcripts/{transcript.id}.pdf')

    if old_file.exists():
        os.remove(f'{settings.MEDIA_ROOT}transcripts/{transcript.id}.pdf')

    transcript.signature    =   signature
    transcript.storage  =   File(file, name=f'{transcript.id}.pdf')
    transcript.save()
