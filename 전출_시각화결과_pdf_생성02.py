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


pdfmetrics.registerFont(TTFont("맑은고딕", "Malgun.ttf"))
pdfmetrics.registerFont(TTFont("맑은고딕체", "Malgunbd.ttf"))


dir_nm = "c:/projects/kosis_dn/광역_전입사유_plot01/"
title_txt = "광역 전입사유별 순위변동 추이 Revisited4"

# 1) 프레임 생성
landscape(A4)[0], landscape(A4)[1]
page_width, page_height = landscape(A4)

frame_width = page_width - 2 * cm  # 프레임 너비를 페이지 너비보다 작게 설정
frame_height = page_height - 2 * cm  # 프레임 높이를 페이지 높이보다 작게 설정

# 첫 번째 페이지 프레임
first_page_frame = Frame(cm, cm, frame_width, frame_height, id='first_page_frame')

# 이후 페이지 프레임
later_pages_frame = Frame(cm, cm, frame_width, frame_height, id='later_pages_frame')

file_list = os.listdir(dir_nm)
png_list = [file for file in file_list if file.endswith(".png")]

class NumberedPageTemplate(PageTemplate):
    def beforeDrawPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('맑은고딕', 10)
        page_number_text = f"Page {doc.page}"
        canvas.drawString(page_width - 100, 30, page_number_text)
        canvas.restoreState()

class TitlePage(Flowable):
    def draw(self):
        canvas = self.canv
        canvas.setFont('맑은고딕체', 20)
        canvas.drawCentredString(page_width / 2, page_height - 50, title_txt)
        canvas.setFont('맑은고딕', 12)
        date_str = datetime.now().strftime("%Y-%m-%d")
        canvas.drawCentredString(page_width / 2, page_height - 80, date_str)

def onFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('맑은고딕체', 20)
    canvas.drawCentredString(page_width / 2, page_height - 50, title_txt)
    canvas.setFont('맑은고딕', 12)
    date_str = datetime.now().strftime("%Y-%m-%d")
    canvas.drawCentredString(page_width / 2, page_height - 80, date_str)
    canvas.restoreState()

def onLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('맑은고딕', 10)
    page_number_text = f"Page {doc.page}"
    canvas.drawString(page_width - 100, 30, page_number_text)
    canvas.restoreState()

doc = BaseDocTemplate(str(dir_nm + title_txt + '.pdf'), pagesize=landscape(A4))

# 첫 번째 페이지 템플릿
first_page_template = PageTemplate(id='FirstPage', frames=[first_page_frame], onPage=onFirstPage)

# 이후 페이지 템플릿
later_pages_template = PageTemplate(id='LaterPages', frames=[later_pages_frame], onPage=onLaterPages)

# 템플릿 추가
doc.addPageTemplates([first_page_template, later_pages_template])

# 첫 번째 페이지에 제목과 날짜 추가
L = [TitlePage(), Spacer(1, 2*cm)]  # TitlePage와 Spacer를 첫 번째 페이지에 추가

# 두 번째 페이지부터 이미지 추가
for num, file in enumerate(png_list):
    print(num, file)
    im = Image.open(dir_nm + file)
    nm = file.split(".")[0]
    imgdata = BytesIO(im.tobytes())
    im.save(imgdata, 'PNG')
    imgdata.seek(0)
    # 이미지 크기를 프레임 크기에 맞게 조정
    image = platypus.Image(imgdata, width=frame_width, height=frame_height)
    L.append(image)

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



