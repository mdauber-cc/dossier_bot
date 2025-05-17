import os
import time
from openai import OpenAI

class DossierGenerator:
    """
    A tool to generate comprehensive dossiers on individuals using OpenAI's search-enabled models.
    """
    
    def __init__(self):
        """Initialize with OpenAI API key from environment variables."""
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it as OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.search_model = "gpt-4o-search-preview"  # Model with web search capabilities
    
    def generate_dossier(self, name, organization):
        """
        Generate a comprehensive dossier on an individual based on their name and organization.
        
        Args:
            name: Full name of the person
            organization: Organization the person is affiliated with
            
        Returns:
            A string containing the complete dossier
        """
        print(f"Generating dossier for {name} at {organization}...")
        
        # Define the main sections we want to cover in our dossier
        sections = [
            "Business and Professional Background",
            "Previous Affiliations and Notable Projects",
            "Areas of Research and Publications",
            "Key Public Statements and Views",
            "Personal Background (Education and Interests)",
            "Media Coverage and Contributions to the Community",
            "Social Media and Online Presence"
        ]
        
        # Collect research for each section
        section_content = {}
        for section in sections:
            print(f"Researching: {section}...")
            section_content[section] = self._research_section(name, organization, section)
            
        # Compile the final dossier
        dossier = self._compile_dossier(name, organization, section_content)
        
        print("Dossier generation complete!")
        return dossier
        
    def _research_section(self, name, organization, section):
        """
        Research a specific section of the dossier using multiple web searches.
        
        Args:
            name: Person's name
            organization: Their organization
            section: The section to research
            
        Returns:
            Combined research findings for the section
        """
        # Define different search angles for each section to get broader coverage
        search_angles = [
            f"Comprehensive overview of {name}'s {section.lower()} at {organization}",
            f"Latest information about {name}'s {section.lower()}",
            f"Detailed analysis of {name}'s {section.lower()} history and background"
        ]
        
        # Additional specific angles based on section type
        if section == "Business and Professional Background":
            search_angles.append(f"{name} career timeline and achievements")
            search_angles.append(f"{name} current role and responsibilities at {organization}")
            
        elif section == "Previous Affiliations and Notable Projects":
            search_angles.append(f"{name} previous companies and roles before {organization}")
            search_angles.append(f"{name} major projects and contributions")
            
        elif section == "Areas of Research and Publications":
            search_angles.append(f"{name} research papers and publications")
            search_angles.append(f"{name} academic contributions and areas of expertise")
            
        elif section == "Key Public Statements and Views":
            search_angles.append(f"{name} interviews and public statements")
            search_angles.append(f"{name} opinions on industry trends and future")
            
        elif section == "Personal Background (Education and Interests)":
            search_angles.append(f"{name} education and academic background")
            search_angles.append(f"{name} personal interests and activities")
            
        elif section == "Media Coverage and Contributions to the Community":
            search_angles.append(f"{name} media appearances and news coverage")
            search_angles.append(f"{name} community involvement and contributions")
            
        elif section == "Social Media and Online Presence":
            search_angles.append(f"{name} social media profiles and activity")
            search_angles.append(f"{name} online presence and digital footprint")
        
        # Collect results from multiple searches
        results = []
        for i, angle in enumerate(search_angles):
            print(f"  Research angle {i+1}/{len(search_angles)}: {angle}")
            
            # Create a tailored prompt for this research angle
            prompt = f"""
            I need you to act as a professional intelligence researcher compiling information about {name} who works at/is affiliated with {organization}.
            
            Focus specifically on: "{angle}"
            This is for the dossier section: "{section}"
            
            Please provide detailed, factual information with citations and include:
            1. Key facts and timeline
            2. Notable achievements or events
            3. Any relevant connections or relationships
            4. Sources where this information can be verified
            
            Format your response in clear paragraphs with bullet points where appropriate.
            Only include information that would reasonably be available through public sources.
            Cite your sources with specific links or references when possible.
            """
            
            # Use the search-enabled model for web research
            response = self.client.chat.completions.create(
                model=self.search_model,
                messages=[
                    {"role": "developer", "content": "You are a professional intelligence analyst with expertise in compiling detailed dossiers on individuals. Provide comprehensive, factual information with precise citations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            
            results.append(response.choices[0].message.content)
        
        # Now deduplicate and synthesize the results
        print(f"  Synthesizing {len(results)} research angles for {section}...")
        
        synthesis_prompt = f"""
        I have multiple research results on {name} focused on the section "{section}". 
        Please synthesize these into a single comprehensive, well-organized section for a professional dossier.
        
        Remove any duplicated information, resolve any contradictions by favoring more recent or authoritative sources,
        and organize the information in a logical format with clear paragraphs where appropriate.
        
        Maintain all relevant source citations and organize the information to flow naturally.
        
        Here are the research results to synthesize:
        
        ---------------------------------------------------
        {results[0]}
        ---------------------------------------------------
        {results[1]}
        ---------------------------------------------------
        {results[2]}
        """
        
        if len(results) > 3:
            synthesis_prompt += f"""
        ---------------------------------------------------
        {results[3]}
            """
            
        if len(results) > 4:
            synthesis_prompt += f"""
        ---------------------------------------------------
        {results[4]}
            """
        
        synthesis_response = self.client.chat.completions.create(
            model="gpt-4-turbo",  # Using standard model for synthesis
            messages=[
                {"role": "user", "content": synthesis_prompt}
            ],
            max_tokens=3000
        )
        
        return synthesis_response.choices[0].message.content
        
        return response.choices[0].message.content
        
    def _compile_dossier(self, name, organization, section_content):
        """
        Compile the final dossier from all the section research.
        
        Args:
            name: Person's name
            organization: Their organization
            section_content: Dictionary containing content for each section
            
        Returns:
            The compiled dossier
        """
        # Create a title for the dossier
        dossier = f"Dossier: {name}\n\n"
        
        # Add each section with its content
        for section, content in section_content.items():
            dossier += f"{section}\n{content}\n\n"
            
        # Add generation timestamp
        dossier += f"---\nDossier generated on {time.strftime('%Y-%m-%d')} using AI-assisted research methods."
        
        return dossier
        
    def save_dossier(self, dossier, name, output_file=None):
        """
        Save the dossier to a file.
        
        Args:
            dossier: The dossier text
            name: Name of the person
            output_file: Optional filename to save to
            
        Returns:
            The path to the saved file
        """
        if not output_file:
            safe_name = name.replace(" ", "_").lower()
            output_file = f"{safe_name}_dossier.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(dossier)
        
        print(f"Dossier saved to {output_file}")
        return output_file


def generate_person_dossier(name, organization, save_to_file=True):
    """
    Generate a comprehensive dossier on an individual.
    
    Args:
        name: Full name of the person
        organization: Organization the person is affiliated with
        save_to_file: Whether to save the dossier to a file
        
    Returns:
        The generated dossier text
    """
    try:
        generator = DossierGenerator()
        dossier = generator.generate_dossier(name, organization)
        
        if save_to_file:
            generator.save_dossier(dossier, name)
        
        return dossier
        
    except Exception as e:
        print(f"Error generating dossier: {e}")
        return f"Error generating dossier: {e}"


# Example usage
if __name__ == "__main__":
    # Set your OpenAI API key
    # os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    
    # Generate a dossier
    dossier = generate_person_dossier("Igor Babushkin", "xAI")