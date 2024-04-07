from pybtex.database.input import bibtex


def get_personal_data():
    name = ["Amy", "Bland"]
    email = "amybland9@gmail.com"
    github = "amy-bland"
    linkedin = "amyf-bland"
    
    # NOTE: Optionally add in the future
    scholar = "scholar_id"
    twitter = "twitter_id"
    youtube = "youtube_id"
    
    bio_text = f"""
    
                <p>
                    I am a Masters student in Politics and Public Administration at the <a href="https://www.uni-konstanz.de/" target="_blank">University of Konstanz</a>.
                <p>
                    <span style="font-weight: bold;">Bio:</span>
                    In 2021, I earned my bachelor's degree from <a href="https://www.monash.edu/" target="_blank">Monash University</a> in Melbourne, Australia, with a focus on Human Rights. 
                    I spent a semester abroad at the <a href="https://uni-tuebingen.de/" target="_blank">University of Tübingen</a> during my undergraduate studies. 
                    I embraced extracurricular activities, including learning Australian Sign Language and serving as a <a href="https://www.unmgcy.org/" target="_blank">United Nations Major Group for Children and Youth</a> country leader for Australia. 
                    Currently, I'm a member of the <a href="https://yjea.org/" target="_blank">Young Journal of European Affairs</a> editorial board and pursuing my master's in Politics and Public Administration at the <a href="https://www.uni-konstanz.de/" target="_blank">University of Konstanz</a>. My research primarily revolves around conflict and development. I am keenly interested in how conflict disproportionately affects women's and children's education and health outcomes.

                </p>
                <p>For any inquiries, feel free to write an email!</p>
                <p>
                    <!-- <a href="https://amy-bland.github.io/assets/pdf/cv_name.pdf" target="_blank" style="margin-right: 15px"><i class="fa fa-address-card fa-lg"></i> CV</a> -->
                    <a href="mailto:{email}" style="margin-right: 15px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <!--  <a href="https://scholar.google.com/citations?user={scholar}&hl=en" target="_blank" style="margin-right: 15px"><i class="fa-solid fa-graduation-cap"></i> Scholar</a> -->
                    <a href="https://github.com/{github}" target="_blank" style="margin-right: 15px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <!--  <a href="https://twitter.com/{twitter}" target="_blank" style="margin-right: 15px"><i class="fab fa-x-twitter fa-lg"></i> Twitter</a> -->
                    <a href="https://www.linkedin.com/in/{linkedin}" target="_blank" style="margin-right: 15px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                    <!-- <a href="https://www.youtube.com/{youtube}" target="_blank" style="margin-right: 15px"><i class="fab fa-youtube fa-lg"></i> YouTube</a> -->
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <h4>Template</h4>
                <p>
                    This page is based on the template of <a href="https://m-niemeyer.github.io/" target="_blank">Michael Niemeyer</a>. Checkout his <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">GitHub repository</a> for instructions on how to use it.</a><br>
                </p>
            </div>
    """
    return name, bio_text, footer


def get_author_dict():
    # Name your co-authors here
    return {
        'Daniel Dauner': 'https://danieldauner.github.io/',
    }


def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Amy Bland', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'):
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s


def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        if 'html' in entry.fields.keys():
            s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""
        else:
            s += f"""{entry.fields['title']} <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    if 'booktitle' in entry.fields.keys():
        s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""
    elif 'journal' in entry.fields.keys():
        s += f"""<span style="font-style: italic;">{entry.fields['journal']}</span>, {entry.fields['year']} <br>"""
    else:
        s += f"""<span style="font-style: italic;">{entry.fields['school']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1

    cite = f"<pre><code>@{entry.original_type}{{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year', 'school', 'journal', 'volume']:
        if entr in entry.fields.keys():
            cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s


def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s


def get_uni_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    # s += f"""{entry.fields['title']}<br>"""
    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        if 'html' in entry.fields.keys():
            s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""
        else:
            s += f"""{entry.fields['title']} <br>"""
    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    
    if 'school' in entry.fields.keys():
        s += f"""<span style="font-style: italic;">{entry.fields['school']}</span>, {entry.fields['year']} <br>"""
    elif 'booktitle' in entry.fields.keys():
        s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""
    
    artefacts = {'pdf': 'Paper', 'video': 'Video', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    

    cite = f"<pre><code>@{entry.original_type}{{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year', 'school', 'journal', 'volume']:
        if entr in entry.fields.keys():
            cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s


def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_paper_entry(k, bib_data.entries[k])
    return s


def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_talk_entry(k, bib_data.entries[k])
    return s


def get_uni_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('uni_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_uni_entry(k, bib_data.entries[k])
    return s


def get_index_html():
    pub = get_publications_html()
    talks = get_talks_html()
    uni = get_uni_html()
    name, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
</head>
<body>
    <div class="container">
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 1em;">
            <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
            </div>
            <br>
            <div class="col-md-8" style="">
                {bio_text}
            </div>
            <div class="col-md-4" style="">
                <img src="assets/img/profile.jpg" class="img-thumbnail" width="280px" alt="Profile picture">
            </div>
        </div>
        <!-- <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Talks</h4>
                {talks}
            </div>
        </div>  -->
        <!--
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Publications</h4>
                {pub}
            </div>
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>University Projects</h4>
                {uni}
            </div>
        </div>  -->
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4><b>News</b></h4>
                 <table>
                     <tr>
                       <td>May, 2024 &#8194;</td>
                       <td> I started my Masters thesis at the <a href="https://www.polver.uni-konstanz.de/hoeffler/" target="_blank">Development Research Group</a>, supervised by <a href="https://www.polver.uni-konstanz.de/hoeffler/team/prof-dr-anke-hoeffler/" target="_blank">Prof. Anke Hoeffler</a>.
                     </tr>
                </table> 
                    
            </div>
        </div>
        <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
            {footer}
        </div>
    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>
</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')


if __name__ == '__main__':
    write_index_html('index.html')
