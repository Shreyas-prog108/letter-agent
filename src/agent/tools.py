import os
import pandas as pd
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Constants
DATA_PATH = "data/"
DB_PATH = "db/"

# -----------------------------
# 🔹 Helper: Get employee metadata
# -----------------------------
def _get_employee_data_logic(employee_name: str) -> dict:
    df = pd.read_csv(os.path.join(DATA_PATH, "Employee_List.csv"))
    employee_details = df[df['Employee Name'].str.lower() == employee_name.lower()]
    if not employee_details.empty:
        return employee_details.to_dict(orient='records')[0]
    else:
        return {"error": f"Employee '{employee_name}' not found."}

# -----------------------------
# 🔹 Helper: Query policy docs
# -----------------------------
def _get_policy_info_logic(query: str) -> str:
    vector_store = FAISS.load_local(
        folder_path=DB_PATH,
        embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        allow_dangerous_deserialization=True  # Add this argument
    )
    retriever = vector_store.as_retriever(search_kwargs={'k': 1})
    relevant_docs = retriever.invoke(query)
    return relevant_docs[0].page_content if relevant_docs else f"No policy info found for query: {query}"

# -----------------------------
# ✅ Main Tool: Agent uses this
# -----------------------------
@tool
def get_all_information_for_offer_letter(employee_name: str) -> str:
    """
    Retrieves all necessary HR policy and employee data to generate an offer letter.
    """
    print(f"--- Running Master Tool for: {employee_name} ---")
    employee_data = _get_employee_data_logic(employee_name)
    if "error" in employee_data:
        return employee_data["error"]

    band = employee_data.get("Band")
    department = employee_data.get("Department")
    leave_policy = _get_policy_info_logic(f"leave policy for Band {band}")
    wfo_policy = _get_policy_info_logic(f"work from office policy for {department}")
    travel_policy = _get_policy_info_logic(f"travel policy for Band {band}")

    full_context = f"""
--- Employee Data ---
{employee_data}

--- Leave Policy Context ---
{leave_policy}

--- Work From Office Policy Context ---
{wfo_policy}

--- Travel Policy Context ---
{travel_policy}
"""

    print("--- Master Tool finished. Returning all context. ---")
    return full_context
