"""
code for running operation type tests
"""
import json


def parse_test_response(response):
    if response["result"] == "error":
        if response["error_type"] == "error":
            # response.message
            pass
        elif response["error_type"] == "assertion_failure":
            # "Test failure: " response.message
            pass
        elif response["error_type"] == "protocol_syntax_error":
            # "Syntax error in protocol: " response.message
            pass
        elif response["error_type"] == "protocol_error":
            # "Execution error in protocol: " response.message
            pass
        elif response["error_type"] == "test_syntax_error":
            # "Syntax error in test: "
            pass
        elif response["error_type"] == "test_error":
            # "Execution error in test: "
            pass

       # for entry in response.exception_backtrace:
       #     pass
    else:
        print("All tests passed")

#    print(response.log)
#show messages on the screen -- send things to std out 
# or turning json into markdown 

    print(response["backtrace"])
    print(len(response["backtrace"]))
    # response.backtrace
    time = None
    for entry in response["backtrace"]:
        print("-------------")
        print(type(entry))
        print(entry)
        print("____________")
        if entry["operation"] == "display":
#            # previous value of time
            for show_object in entry["content"]:
                print(show_object)
                print("_____")
#                # see showmatch in markdown converter
#                # "line" is object {"key": "value"}
#            time = entry["time"]
#        elif entry["operation"] == "error":
#            print("error") # see error.md
#        else:
#            print("asdfasfasdfasasadfas")
#
def format_table(content):
    formatted = ["<table>"]
    ary = json.loads(content)
    style = "border: 1px solid gray; text-align: center"
    for row in ary:
        newrow = ""
        for cell in row:
            this_style = style

            if isinstance(cell, dict):
                newcell = cell.get("content") or "?"
                if cell.get("class") == "td-filled-slot":
                    this_style = style + "; background-color: lightskyblue"

            else:
                newcell = cell

            newrow += "<td style=\"{}\">{}</td>".format(this_style, newcell)
        formatted.append("<tr>{}</tr>".format(newrow))

    formatted.append("</table>")
    
    return formatted
