

def html_table(table_data):
    html = f"""<div class ="table-responsive">
<table class ="table table-striped table-sm" id="quick_cruise_table">
<thead>
<tr>
"""
    for i in table_data[0]:
        html += f"""<th><label>{i}</label></th>\n"""
    html += """</tr>\n</thead>\n<tbody>\n"""

    for i in table_data[1:]:
        html += f"""<tr style = "cursor: pointer;" onclick = "window.location='{{ url_for('purchaser', purchaser_name={i[0]}) }}'"\n>"""
        for j in i:
            html += f"""<td><label> {j} </label></td>\n"""
    html += """</tr>
</tbody>
</table>
</div>
"""
    return html