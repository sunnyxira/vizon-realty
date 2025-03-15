document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('textarea.trix-content').forEach((textarea) => {
        let input = document.createElement("input");
        input.setAttribute("id", textarea.id);
        input.setAttribute("name", textarea.name);
        input.setAttribute("type", "hidden");

        let trixEditor = document.createElement("trix-editor");
        trixEditor.setAttribute("input", textarea.id);

        textarea.replaceWith(input);
        input.insertAdjacentElement("afterend", trixEditor);
    });
});
