"""
Create a sample PDF for testing.

This generates a simple PDF report you can use to test the chatbot.
Run: python data/sample_report.py

Requires: pip install fpdf2
"""

try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf2...")
    import subprocess
    subprocess.check_call(["pip", "install", "fpdf2"])
    from fpdf import FPDF


class SampleReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Machine Learning Basics - Sample Report', 0, 1, 'C')
        self.ln(5)
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(2)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()


def create_sample_pdf():
    """Create a sample PDF about machine learning."""
    
    pdf = SampleReport()
    pdf.add_page()
    
    # Title Page
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 20, 'Introduction to Machine Learning', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'A Beginner\'s Guide', 0, 1, 'C')
    pdf.ln(20)
    
    # Chapter 1
    pdf.chapter_title('1. What is Machine Learning?')
    pdf.chapter_body(
        "Machine Learning (ML) is a subset of Artificial Intelligence that enables "
        "computers to learn and improve from experience without being explicitly programmed. "
        "Instead of following strict rules, ML algorithms build mathematical models from "
        "sample data to make predictions or decisions.\n\n"
        "The key idea is that given enough data, a machine learning model can identify "
        "patterns and relationships that would be difficult or impossible for humans to "
        "explicitly code. This makes ML particularly useful for complex problems like "
        "image recognition, natural language processing, and recommendation systems."
    )
    
    # Chapter 2
    pdf.chapter_title('2. Types of Machine Learning')
    pdf.chapter_body(
        "There are three main types of machine learning:\n\n"
        "SUPERVISED LEARNING: The algorithm learns from labeled training data. "
        "Each example includes input features and the correct output. The model "
        "learns to map inputs to outputs. Examples include spam detection and "
        "house price prediction.\n\n"
        "UNSUPERVISED LEARNING: The algorithm finds patterns in unlabeled data. "
        "It discovers hidden structures without predefined categories. Examples "
        "include customer segmentation and anomaly detection.\n\n"
        "REINFORCEMENT LEARNING: The algorithm learns by interacting with an "
        "environment, receiving rewards or penalties for actions. It's used in "
        "game playing, robotics, and autonomous systems."
    )
    
    # Chapter 3
    pdf.chapter_title('3. Key Algorithms')
    pdf.chapter_body(
        "LINEAR REGRESSION: Used for predicting continuous values. It finds the "
        "best-fitting straight line through data points. Common in sales forecasting "
        "and risk assessment.\n\n"
        "DECISION TREES: Tree-like models that make decisions based on feature values. "
        "Easy to interpret but prone to overfitting. Often used in medical diagnosis.\n\n"
        "NEURAL NETWORKS: Inspired by biological brains, these consist of interconnected "
        "nodes organized in layers. Deep learning uses many hidden layers for complex "
        "tasks like image and speech recognition.\n\n"
        "SUPPORT VECTOR MACHINES (SVM): Effective for classification tasks, especially "
        "in high-dimensional spaces. Widely used in text classification and bioinformatics."
    )
    
    # Chapter 4
    pdf.chapter_title('4. Applications')
    pdf.chapter_body(
        "Machine learning is transforming industries:\n\n"
        "HEALTHCARE: Disease prediction, drug discovery, medical imaging analysis, "
        "and personalized treatment recommendations.\n\n"
        "FINANCE: Fraud detection, algorithmic trading, credit scoring, and "
        "risk management.\n\n"
        "RETAIL: Recommendation engines, demand forecasting, and customer churn "
        "prediction.\n\n"
        "TRANSPORTATION: Self-driving cars, route optimization, and predictive "
        "maintenance.\n\n"
        "ENTERTAINMENT: Content recommendations on Netflix and Spotify, game AI, "
        "and content generation."
    )
    
    # Chapter 5
    pdf.chapter_title('5. Conclusion')
    pdf.chapter_body(
        "Machine learning is a powerful tool that's becoming essential in the modern "
        "world. While it requires mathematical understanding and programming skills, "
        "the barriers to entry are lower than ever thanks to libraries like scikit-learn, "
        "TensorFlow, and PyTorch.\n\n"
        "The field continues to evolve rapidly, with new techniques and applications "
        "emerging constantly. Understanding the fundamentals covered in this report "
        "provides a solid foundation for further study and practical application."
    )
    
    # Save
    output_path = "data/sample_ml_report.pdf"
    pdf.output(output_path)
    print(f"✅ Created sample PDF: {output_path}")
    print("\nYou can now upload this PDF to the chatbot and ask questions like:")
    print("- 'What is machine learning?'")
    print("- 'What are the types of machine learning?'")
    print("- 'What are some applications of ML?'")


if __name__ == "__main__":
    create_sample_pdf()
