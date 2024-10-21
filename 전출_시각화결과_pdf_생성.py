import os
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, KeepTogether, Frame
from reportlab.lib.units import cm
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors
from reportlab import platypus
# import requests
import PIL
from io import BytesIO


pdfmetrics.registerFont(TTFont("맑은고딕", "Malgun.ttf"))
pdfmetrics.registerFont(TTFont("맑은고딕체", "Malgunbd.ttf"))

# 1) A4 가로, 세로 사이즈 책정
text_frame = Frame(
            x1=2.54 * cm ,  # From left
            y1=2.54 * cm ,  # From bottom
            height=15.92 * cm,
            width=24.16 * cm,
            leftPadding=0 * cm,
            bottomPadding=0 * cm,
            rightPadding=0 * cm,
            topPadding=0 * cm,
            showBoundary=0,
            id='text_frame'
        )


# 2) 이미지데이터 전처리
dir_nm = "c:/projects/kosis_dn/전출_세대주포함_여부_plot/"
file_list = os.listdir(dir_nm)
png_list = [file for file in file_list if file.endswith(".png")]
for num, file in enumerate(png_list):
    im = Image.open(dir_nm+file)
    nm = file.split(".")[0]
    im.resize((3000,1750)).save(dir_nm + nm +".tiff", format="TIFF")

tiff_list = [file for file in file_list if file.endswith(".tiff")]
tiff_list = sorted(tiff_list)
tiff_list

# 3) PDF 생성
L = []
for num, file in enumerate(tiff_list):
    im = Image.open(dir_nm + file)
    nm = file.split(".")[0]
    imgdata = BytesIO(im.tobytes())
    im.save(imgdata, 'TIFF')
    imgdata.seek(0)
    L.append(platypus.Image(imgdata, width=24.16 * cm, height=15.92 * cm))
    L.append(Paragraph(nm, style=ParagraphStyle(name='Normal', fontName='맑은고딕체', fontSize=20, textColor=colors.black)))

doc = BaseDocTemplate(str('report.pdf'), pagesize=A4)
frontpage = PageTemplate(id='FrontPage',
                     frames=[text_frame]    # 4. 프레임 지정 부분에서 text_frame 생성했음
            )
doc.addPageTemplates(frontpage)
doc.build(L)

