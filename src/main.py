from text_node_to_html_node import *
import os
import shutil
import sys


def copy_source_to_dest(source, destination):
    try:
        #first gets path to source directory, returns errors if cannot access source
        source_path = os.path.abspath(source)
        target_dir_src = os.path.normpath(os.path.join(source_path, "."))
        valid_target_dir_src = os.path.commonpath([source_path, target_dir_src]) == source_path

        if valid_target_dir_src == False:
            return f'Error: Cannot access "{source}" as it is outside the permitted working directory'
        
        #same thing with the destination directory
        dest_path = os.path.abspath(destination)
        target_dir_dest = os.path.normpath(os.path.join(dest_path, "."))
        valid_target_dir_dest = os.path.commonpath([dest_path, target_dir_dest]) == dest_path

        if valid_target_dir_dest == False:
            return f'Error: Cannot access "{destination}" as it is outside the permitted working directory'
        
        #if either of the source or destination are not directories throws error
        
        
        if os.path.isdir(source_path) != True:
            raise Exception("source directory is not valid")
        if os.path.isdir(dest_path) != True:
            raise Exception("destination directory is not valid")
        
        #deletes the destination directory to ensure its clean, then creates a new one of the same name
        shutil.rmtree(dest_path)
        os.mkdir(target_dir_dest)

        for content in os.listdir(target_dir_src):
            content_path = os.path.join(target_dir_src, content)

            if os.path.isdir(content_path):
                new_dir_path = os.path.join(target_dir_dest, content)
                os.mkdir(new_dir_path)
                copy_source_to_dest(content_path, new_dir_path)
            else:
                shutil.copy(content_path, target_dir_dest)

    except Exception as e:
        return f"Error: {e}"
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path) as f:
            from_path_contents = f.read()
        with open(template_path) as f:
            temp_path_contents = f.read()

        node = markdown_to_html_node(from_path_contents)
        html = node.to_html()
        title = extract_title(from_path_contents)

        with_title = temp_path_contents.replace("{{ Title }}", title)
        with_contents = with_title.replace("{{ Content }}", html)
        with_basepath = with_contents.replace('href="/ssg/', f'href="' + basepath)
        with_src = with_basepath.replace('src="/ssg/', f'src="' + basepath)

        temp_file = open(dest_path, "w")
        temp_file.write(with_src)
        temp_file.close()
        
    except Exception as e:
        return f"Error: {e}"

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    try:
        path = os.path.abspath(dir_path_content)
        target_dir_src = os.path.normpath(os.path.join(path, "."))

        for content in os.listdir(target_dir_src):
            content_path = os.path.join(target_dir_src, content)
            if os.path.isdir(content_path):
                new_dir_path = os.path.join(dest_dir_path, content)
                os.mkdir(new_dir_path)
                generate_pages_recursively(content_path, template_path, new_dir_path, basepath)
            elif os.path.isfile(content_path):
                root_path = os.path.splitext(content)
                str = root_path[0]
                str += ".html"
                new_dir_path = os.path.join(dest_dir_path, str)
                generate_page(content_path, template_path, new_dir_path, basepath)

    except Exception as e:
        return f"Error: {e}"
    

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_source_to_dest("./static", "./docs")
    generate_pages_recursively("./content", "./template.html", "./docs", basepath)


main()