import streamlit as st
from econometric_module.upload_file import streamlit_file_uploader

def main():
    st.sidebar.title("Regressly App")
    st.sidebar.markdown("Navigate through the app:")

    # Sidebar Navigation
    menu = ["File Uploader", "Other Feature (Placeholder)"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "File Uploader":
        st.header("📂 File Uploader")
        streamlit_file_uploader()
    elif choice == "Other Feature (Placeholder)":
        st.header("🚧 Under Construction")
        st.write("Additional features coming soon!")

if __name__ == "__main__":
    main()
