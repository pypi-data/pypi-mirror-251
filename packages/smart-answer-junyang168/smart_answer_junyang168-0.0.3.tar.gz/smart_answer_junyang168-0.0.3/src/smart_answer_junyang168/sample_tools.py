from base_tool import base_tool
from tool_example import tool_example
from datetime import date
from tool_selector import tool_selector

class LifeCycleTool(base_tool):
    name = "VMWare production version and life cycle dates"
    description = """ use this tool to understand support dates, general availability date and end of technical guidance date of VMware product versions
        The input to this tool should be  the VMWare product release. Use comma delimited string if question is about multiple releases.
    """
    
    def get_few_shots(self):
        return [
            tool_example("When will vSphere 7 go out of support",'vSphere 7' ),
            tool_example("When will vSphere 7 be released",'vSphere 7' ),
            tool_example("What versions of vShpere are still supported",'vSphere'),
            tool_example("What versions of vShpere are released",'vSphere'),           
        ]
                        
    def get_answer_prompt_template(self,default_prompt, context):
        return  """ General availability Date determines when a specific version of VMWare product is released. The later the General Availability Date, the newer the release. """ + default_prompt 
            
class KB_DocTool(base_tool):
    name = "VMWare Knowledge Base"
    description = """This is the default tool to understand any VMWare product related issues and questions other tools can't handle. 
      Do not use this tool if other tools can answer the question. Use this tool if other tool returns 'Unable to get data'
      The input to this tool should be a comma separated list of string of length two, representing VMware product release and the topics of the question.
      """

    def get_few_shots(self):
        return [
            tool_example("How to configure vGPU in ESXi?",'ESXi, configure vGPU' )
        ]

class InterOperabilityTool(base_tool):
    name = "VMWare Product Compatibility"
    description = """
        use this tool to understand compatibiilty or interoperability between VMWare products.  
        The input to this tool should be a comma separated list of string of length two, representing the two product releases you wanto understand compatibility with.
        For example, 
            1. `Aria 1.0,ESXi 5.0` would be the input if you wanted to know whether VMware Aria 1.0  can run on VMware ESXi 5.0. 
            2. `Aria,ESXi 5.0` would be the input if you wanted to know the versions of Aria that support VMware ESXi 5.0. 
    """

    def get_few_shots(self):
        return [
            tool_example("Is vSAN compatible with vCenter?",'vSAN, vCenter' )
        ]

