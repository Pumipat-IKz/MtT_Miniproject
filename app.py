
import streamlit as st
from PIL import Image
from io import BytesIO

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="JPG to PDF",
    page_icon="📄",
    layout="centered"
)

# ขนาดกระดาษ หน่วย points (72 points = 1 inch)
PAPER_SIZES = {
    "A4": (595.28, 841.89),
    "A3": (841.89, 1190.55),
    "A5": (419.53, 595.28),
    "Letter": (612, 792)
}


# ปรับภาพให้พอดีกับหน้ากระดาษ
def fit_image(image, size):
    page_w, page_h = size
    image = image.convert("RGB")

    scale = min(
        page_w / image.width,
        page_h / image.height
    )

    new_size = (
        max(1, round(image.width * scale)),
        max(1, round(image.height * scale))
    )

    image = image.resize(
        new_size,
        Image.Resampling.LANCZOS
    )

    page = Image.new(
        "RGB",
        (round(page_w), round(page_h)),
        "white"
    )

    x = (page.width - image.width) // 2
    y = (page.height - image.height) // 2
    page.paste(image, (x, y))

    return page


# หัวข้อเว็บ
st.title("JPG to PDF Converter")
st.caption("Convert images into one PDF file.")
st.divider()


# อัปโหลดรูปภาพ
uploaded_files = st.file_uploader(
    "เลือกภาพที่ต้องการแปลง",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)


if uploaded_files:

    # สร้างรายการไฟล์สำหรับใช้ในเซสชันนี้
    current_files = {
        f"{i}_{file.name}_{file.size}": file
        for i, file in enumerate(uploaded_files)
    }

    current_keys = list(current_files.keys())

    # เก็บลำดับรูปภาพ
    if (
        "image_order" not in st.session_state
        or set(st.session_state.image_order) != set(current_keys)
    ):
        st.session_state.image_order = current_keys.copy()

    st.success(f"เลือกรูปแล้ว {len(uploaded_files)} รูป")

    # เลือกขนาดกระดาษ
    paper_size = st.selectbox(
        "ขนาดกระดาษ",
        ["A4", "A3", "A5", "Letter", "Original"],
        index=0
    )

    st.caption(
        "รูปภาพจะถูกปรับให้พอดีกับหน้ากระดาษ "
        "โดยรักษาสัดส่วนเดิมไว้"
    )

    st.divider()
    st.subheader("ตัวอย่างและจัดลำดับรูปภาพ")

    # แสดงรูปและปุ่มเลื่อนลำดับ
    for i, key in enumerate(st.session_state.image_order):
        file = current_files[key]

        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.image(
                    file.getvalue(),
                    use_container_width=True
                )

            with col2:
                st.write(f"**หน้า {i + 1}**")
                st.caption(file.name)

            with col3:
                if st.button(
                    "▲ เลื่อนขึ้น",
                    key=f"up_{key}",
                    disabled=(i == 0),
                    use_container_width=True
                ):
                    order = st.session_state.image_order
                    order[i - 1], order[i] = order[i], order[i - 1]
                    st.rerun()

                if st.button(
                    "▼ เลื่อนลง",
                    key=f"down_{key}",
                    disabled=(
                        i == len(st.session_state.image_order) - 1
                    ),
                    use_container_width=True
                ):
                    order = st.session_state.image_order
                    order[i], order[i + 1] = order[i + 1], order[i]
                    st.rerun()

    st.divider()

    # แปลงรูปภาพเป็น PDF
    if st.button(
        "แปลงเป็น PDF",
        use_container_width=True
    ):
        try:
            images = []

            for key in st.session_state.image_order:
                file = current_files[key]

                image = Image.open(
                    BytesIO(file.getvalue())
                ).convert("RGB")

                if paper_size != "Original":
                    image = fit_image(
                        image,
                        PAPER_SIZES[paper_size]
                    )

                images.append(image)

            if images:
                pdf_buffer = BytesIO()

                images[0].save(
                    pdf_buffer,
                    format="PDF",
                    save_all=True,
                    append_images=images[1:]
                )

                st.session_state["pdf_data"] = (
                    pdf_buffer.getvalue()
                )
                st.session_state["pdf_name"] = "converted.pdf"

                st.success("แปลงไฟล์สำเร็จแล้ว!")

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")

    # ปุ่มดาวน์โหลด
    if "pdf_data" in st.session_state:
        st.download_button(
            "ดาวน์โหลด PDF",
            data=st.session_state["pdf_data"],
            file_name=st.session_state["pdf_name"],
            mime="application/pdf",
            use_container_width=True
        )

else:
    st.info("กรุณาอัปโหลดรูปภาพ JPG หรือ PNG")

    # ล้างข้อมูล PDF เมื่อไม่มีรูป
    st.session_state.pop("pdf_data", None)
    st.session_state.pop("pdf_name", None)
    st.session_state.pop("image_order", None)


# เครดิตมุมขวาล่าง
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
