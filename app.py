
import streamlit as st
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="JPG to PDF",
    page_icon="📄",
    layout="centered"
)

if "image_order" not in st.session_state:
    st.session_state.image_order = []

st.title("JPG to PDF Converter")
st.caption("Convert images into one PDF file.")
st.divider()

uploaded_files = st.file_uploader(
    "เลือกภาพที่ต้องการแปลง",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    # เก็บลำดับไฟล์ตามชื่อไฟล์และเนื้อหา
    current_files = {
        f"{file.name}_{file.size}_{i}": file
        for i, file in enumerate(uploaded_files)
    }

    # เริ่มต้นลำดับเมื่อมีการอัปโหลดไฟล์
    current_keys = list(current_files.keys())

    if (
        not st.session_state.image_order
        or set(st.session_state.image_order) != set(current_keys)
    ):
        st.session_state.image_order = current_keys.copy()

    st.write(f"จำนวนรูปภาพ: {len(uploaded_files)} รูป")
    st.subheader("จัดลำดับรูปภาพ")

    for i, key in enumerate(st.session_state.image_order):
        file = current_files[key]

        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                st.image(file.getvalue(), use_container_width=True)

            with col2:
                st.write(f"**หน้า {i + 1}**")
                st.caption(file.name)

            with col3:
                if st.button(
                    "▲",
                    key=f"up_{key}",
                    disabled=(i == 0),
                    use_container_width=True
                ):
                    order = st.session_state.image_order
                    order[i - 1], order[i] = order[i], order[i - 1]
                    st.rerun()

                if st.button(
                    "▼",
                    key=f"down_{key}",
                    disabled=(i == len(st.session_state.image_order) - 1),
                    use_container_width=True
                ):
                    order = st.session_state.image_order
                    order[i], order[i + 1] = order[i + 1], order[i]
                    st.rerun()

    st.divider()

    if st.button("แปลงเป็น PDF", use_container_width=True):
        try:
            images = []

            for key in st.session_state.image_order:
                file = current_files[key]
                image = Image.open(BytesIO(file.getvalue())).convert("RGB")
                images.append(image)

            if images:
                pdf_buffer = BytesIO()

                images[0].save(
                    pdf_buffer,
                    format="PDF",
                    save_all=True,
                    append_images=images[1:]
                )

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
    st.session_state.image_order = []
    st.info("กรุณาอัปโหลดรูปภาพ JPG หรือ PNG")

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
