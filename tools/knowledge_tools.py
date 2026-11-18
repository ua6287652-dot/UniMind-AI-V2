from langchain_core.tools import tool
def make_tools(kb):
    def fmt(docs):
        if not docs: return "No matching evidence found in uploaded documents."
        return "\\n\\n".join(f"[Source: {d.metadata.get('source','Unknown')}; page: {d.metadata.get('page','N/A')}]\\n{d.page_content}" for d in docs)
    @tool
    def search_university_documents(query:str)->str:
        """Search all university documents for relevant evidence."""
        return fmt(kb.search(query))
    @tool
    def search_admission_policy(query:str)->str:
        """Search admission eligibility, application requirements, deadlines and prospectus."""
        docs=kb.search(query+" admission eligibility application prospectus")
        filtered=[d for d in docs if any(x in d.metadata.get("source","").lower() for x in ["admission","prospectus","handbook"])]
        return fmt(filtered or docs)
    @tool
    def search_fee_structure(query:str)->str:
        """Search tuition, semester fees, scholarships and payment information."""
        docs=kb.search(query+" fee tuition semester payment scholarship")
        filtered=[d for d in docs if any(x in d.metadata.get("source","").lower() for x in ["fee","prospectus","handbook"])]
        return fmt(filtered or docs)
    @tool
    def search_courses_and_departments(query:str)->str:
        """Search degree programs, departments and course outlines."""
        docs=kb.search(query+" courses departments program curriculum")
        filtered=[d for d in docs if any(x in d.metadata.get("source","").lower() for x in ["course","department","prospectus"])]
        return fmt(filtered or docs)
    @tool
    def summarize_university_material(query:str)->str:
        """Retrieve relevant university text to summarize."""
        return fmt(kb.search(query,k=8))
    @tool
    def compare_university_information(query:str)->str:
        """Retrieve evidence for comparing programs, fees or policies."""
        return fmt(kb.search(query,k=8))
    return [search_university_documents,search_admission_policy,search_fee_structure,search_courses_and_departments,summarize_university_material,compare_university_information]
