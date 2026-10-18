
import streamlit as st
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="JPG to PDF",
    page_icon="📄",
    layout="centered"
)

st.title("JPG to PDF Converter")
st.caption("Convert multiple images into one PDF file.")
st.divider()

uploaded_files = st.file_uploader(
    "เลือกภาพที่ต้องการแปลง",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"เลือกรูปแล้ว {len(uploaded_files)} รูป")

    with st.expander("ดูรายการรูปภาพ"):
        for file in uploaded_files:
            st.write(f"🖼️ {file.name}")

    if st.button("แปลงเป็น PDF", use_container_width=True):
        try:
            images = []

            for file in uploaded_files:
                image = Image.open(file).convert("RGB")
                images.append(image)

            pdf_buffer = BytesIO()
            images[0].save(
                pdf_buffer,
                format="PDF",
                save_all=True,
                append_images=images[1:]
            )

            st.success("แปลงไฟล์สำเร็จแล้ว!")

            st.download_button(
                "ดาวน์โหลด PDF",
                data=pdf_buffer.getvalue(),
                file_name="converted.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("กรุณาอัปโหลดรูปภาพ JPG หรือ PNG เพื่อเริ่มต้น")

st.divider()

st.markdown(
    """
    <div style="
        text-align: right;
        color: gray;
        font-size: 11px;
        margin-top: 10px;
    ">
        Pumipat Wattanapan | MtT 6903016410339
    </div>
    """,
    unsafe_allow_html=True
)
