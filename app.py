
import streamlit as st
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="JPG to PDF", page_icon="📄")

PAPER = {
    "A4": (595, 842), "A3": (842, 1191),
    "A5": (420, 595), "Letter": (612, 792)
}

def fit_image(img, size):
    img = img.convert("RGB")
    w, h = size
    scale = min(w / img.width, h / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)),
                     Image.Resampling.LANCZOS)
    page = Image.new("RGB", size, "white")
    page.paste(img, ((w - img.width) // 2, (h - img.height) // 2))
    return page

st.title("JPG to PDF Converter")
st.caption("Convert images into one PDF file.")
files = st.file_uploader(
    "เลือกภาพที่ต้องการแปลง",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if files:
    keys = [f"{i}_{f.name}_{f.size}" for i, f in enumerate(files)]
    data = dict(zip(keys, files))

    if ("order" not in st.session_state
            or set(st.session_state.order) != set(keys)):
        st.session_state.order = keys.copy()

    size = st.selectbox(
        "ขนาดกระดาษ", ["A4", "A3", "A5", "Letter", "Original"]
    )
    st.write(f"เลือกรูปแล้ว {len(files)} รูป")
    st.subheader("ตัวอย่างและจัดลำดับรูปภาพ")

    for i, key in enumerate(st.session_state.order):
        file = data[key]
        with st.container(border=True):
            a, b, c = st.columns([1, 2, 1])
            a.image(file.getvalue(), use_container_width=True)
            b.write(f"**หน้า {i + 1}**")
            b.caption(file.name)

            if c.button("▲", key=f"up{key}", disabled=i == 0):
                order = st.session_state.order
                order[i - 1], order[i] = order[i], order[i - 1]
                st.rerun()

            if c.button("▼", key=f"down{key}",
                         disabled=i == len(keys) - 1):
                order = st.session_state.order
                order[i], order[i + 1] = order[i + 1], order[i]
                st.rerun()

    if st.button("แปลงเป็น PDF", use_container_width=True):
        try:
            images = []
            for key in st.session_state.order:
                img = Image.open(BytesIO(data[key].getvalue()))
                if size != "Original":
                    img = fit_image(img, PAPER[size])
                else:
                    img = img.convert("RGB")
                images.append(img)

            output = BytesIO()
            images[0].save(output, format="PDF", save_all=True,
                           append_images=images[1:])
            st.session_state.pdf = output.getvalue()
            st.success("แปลงไฟล์สำเร็จ!")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")

    if "pdf" in st.session_state:
        st.download_button("ดาวน์โหลด PDF", st.session_state.pdf,
                           "converted.pdf", "application/pdf",
                           use_container_width=True)
else:
    st.info("กรุณาอัปโหลดรูปภาพ JPG หรือ PNG")
    st.session_state.pop("order", None)
    st.session_state.pop("pdf", None)

st.divider()
st.markdown(
    '<div style="text-align:right;color:gray;font-size:11px">'
    'Pumipat Wattanapan | MtT 6903016410339</div>',
    unsafe_allow_html=True
)
