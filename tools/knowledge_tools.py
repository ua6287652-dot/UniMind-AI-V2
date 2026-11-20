
from langchain_core.tools import tool


def make_tools(kb):

    def format_documents(docs):
        if not docs:
            return "No matching evidence found in uploaded documents."

        results = []

        for doc in docs:
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", None)

            if isinstance(page, int):
                page = page + 1
            else:
                page = "N/A"

            results.append(
                f"[Source: {source}; Page: {page}]\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(results)

    @tool
    def search_university_documents(query: str) -> str:
        """Search all uploaded university documents for relevant information."""
        docs = kb.search(query)
        return format_documents(docs)

    @tool
    def search_admission_policy(query: str) -> str:
        """Search admission eligibility, requirements, deadlines and prospectus."""
        docs = kb.search(
            query + " admission eligibility application requirements prospectus"
        )

        filtered = [
            doc for doc in docs
            if any(
                word in doc.metadata.get("source", "").lower()
                for word in ["admission", "prospectus", "handbook"]
            )
        ]

        return format_documents(filtered or docs)

    @tool
    def search_fee_structure(query: str) -> str:
        """Search tuition fees, semester fees, scholarships and payment information."""
        docs = kb.search(
            query + " fee tuition semester payment scholarship"
        )

        filtered = [
            doc for doc in docs
            if any(
                word in doc.metadata.get("source", "").lower()
                for word in ["fee", "prospectus", "handbook"]
            )
        ]

        return format_documents(filtered or docs)

    @tool
    def search_courses_and_departments(query: str) -> str:
        """Search degree programs, departments and course outlines."""
        docs = kb.search(
            query + " courses departments programs curriculum"
        )

        filtered = [
            doc for doc in docs
            if any(
                word in doc.metadata.get("source", "").lower()
                for word in ["course", "department", "prospectus"]
            )
        ]

        return format_documents(filtered or docs)

    @tool
    def summarize_university_material(query: str) -> str:
        """Retrieve university document evidence for summarization."""
        docs = kb.search(query, k=8)
        return format_documents(docs)

    @tool
    def compare_university_information(query: str) -> str:
        """Retrieve evidence for comparing programs, fees or university policies."""
        docs = kb.search(query, k=8)
        return format_documents(docs)

    return [
        search_university_documents,
        search_admission_policy,
        search_fee_structure,
        search_courses_and_departments,
        summarize_university_material,
        compare_university_information,
    ]
