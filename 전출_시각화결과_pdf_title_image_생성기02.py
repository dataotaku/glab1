import os
from PIL import Image
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, KeepTogether, Frame
from reportlab.lib.units import cm
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors
from reportlab import platypus
# import requests
import PIL
from io import BytesIO
from datetime import datetime
from reportlab.platypus import PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate


pdfmetrics.registerFont(TTFont("맑은고딕", "Malgun.ttf"))
pdfmetrics.registerFont(TTFont("맑은고딕체", "Malgunbd.ttf"))


dir_nm = "c:/projects/kosis_dn/광역_전입사유_plot01/"
title_txt = "광역 전입사유별 순위변동 추이"

# 1) 프레임 생성
landscape(A4)[0], landscape(A4)[1]
page_width, page_height = landscape(A4)

frame_width = landscape(A4)[0]
frame_height = landscape(A4)[1]

text_frame = Frame(0, 0, 
                   frame_width, 
                   frame_height, id='text_frame')


# 2) 이미지데이터 전처리

file_list = os.listdir(dir_nm)
png_list = [file for file in file_list if file.endswith(".png")]


# 타이틀 추가용 문장 추가

sample_style_sheet = getSampleStyleSheet()
# if you want to see all the sample styles, this prints them
# sample_style_sheet.list()

my_title_style = sample_style_sheet['h1']
my_title_style.fontName = '맑은고딕체'
my_title_style.fontSize = 35
my_title_style.alignment = 1
my_title_style.spaceAfter = 5
h1_title = Paragraph(title_txt, my_title_style)
h1_title
my_vis_style = sample_style_sheet['h3']
my_vis_style.fontName = '맑은고딕'
my_vis_style.fontSize = 25
my_vis_style.alignment = 1
my_vis_style.spaceAfter = 5
h3_vis = Paragraph("(시각화 결과 리뷰용 PDF)", my_vis_style)
h3_vis

my_body_style = sample_style_sheet['h6']
my_body_style.fontName = '맑은고딕'
my_body_style.fontSize = 15
my_body_style.alignment = 1
my_body_style.spaceAfter = 5
h6_date = Paragraph(datetime.now().strftime("%Y-%m-%d"), my_body_style)
h6_date

L = []
L.append(Spacer(1, 5*cm))
L.append(h1_title)
L.append(Spacer(1, 2*cm))
L.append(h3_vis)
L.append(Spacer(1, 2*cm))
L.append(h6_date)
L.append(Spacer(1, 5*cm))  # Spacer를 사용하여 공간을 추가
L
for num, file in enumerate(png_list):
    print(num, file)
    im = Image.open(dir_nm + file)
    nm = file.split(".")[0]
    imgdata = BytesIO(im.tobytes())
    im.save(imgdata, 'PNG')
    imgdata.seek(0)
    L.append(platypus.Image(imgdata, width=24.16 * cm, height=15.92 * cm))

class NumberedPageTemplate(PageTemplate):
    def beforeDrawPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('맑은고딕', 10)
        page_number_text = f"{title_txt} Page {doc.page}"
        canvas.drawString(page_width - 300, 30, page_number_text)
        canvas.restoreState()

doc = BaseDocTemplate(str(dir_nm + title_txt + '.pdf'), pagesize=landscape(A4))
image_page = NumberedPageTemplate(id='SinglePage',
                     frames=[text_frame]    # 4. 프레임 지정 부분에서 text_frame 생성했음
            )
doc.addPageTemplates(image_page)
doc.build(L)


# 3) PDF 생성
# L = []
# for num, file in enumerate(png_list):
#     print(num, file)
#     im = Image.open(dir_nm + file)
#     nm = file.split(".")[0]
#     imgdata = BytesIO(im.tobytes())
#     im.save(imgdata, 'PNG')
#     imgdata.seek(0)
#     L.append(platypus.Image(imgdata, width=24.16 * cm, height=15.92 * cm))

# class NumberedPageTemplate(PageTemplate):
#     def beforeDrawPage(self, canvas, doc):
#         canvas.saveState()
#         canvas.setFont('맑은고딕', 10)
#         page_number_text = f"Page {doc.page}"
#         canvas.drawString(page_width - 100, 30, page_number_text)
#         canvas.restoreState()

# class NumberedPageTemplate2(PageTemplate):
#     def beforeDrawPage(self, canvas, doc):
#         canvas.saveState()
#         canvas.setFont('맑은고딕', 10)
#         page_number_text = f"Page {doc.page}"
#         canvas.drawString(page_width - 100, 30, page_number_text)
        
#         # 첫 번째 페이지에 제목과 날짜 추가
#         if doc.page == 1:
#             print("Adding title and date to the first page")  # 디버그용 출력
#             title = title_txt
#             date_str = datetime.now().strftime("%Y-%m-%d")
#             canvas.setFont('맑은고딕체', 20)
#             canvas.drawString(page_width / 2, page_height - 50, title)
#             canvas.setFont('맑은고딕', 12)
#             canvas.drawString(page_width / 2, page_height - 80, date_str)
        
#         canvas.restoreState()

# doc = BaseDocTemplate(str(dir_nm + title_txt + '.pdf'), pagesize=landscape(A4))
# image_page = NumberedPageTemplate2(id='SingleFrame',
#                      frames=[text_frame]    # 4. 프레임 지정 부분에서 text_frame 생성했음
#             )
# doc.addPageTemplates(image_page)
# doc.build(L)



