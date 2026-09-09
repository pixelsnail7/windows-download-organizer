import { Event, getData } from "./utility.mjs";

async function Api(api = "oragnize_files_api") {
  try {
    const response = await fetch(`/${api}`, {
      method: "POST",
    });

    const data = await response.json();

    if (data.success) {
      alert(data.message);
    } else {
      alert(data.error);
    }
  } catch {
    alert("Server error occurred while organizing downloads.");
  }
}

Event("#organize_files_btn", "click", () => Api("oragnize_files_api"));
Event("#remove_empty_folders_btn", "click", () => Api("remove_empty_folders_api"));
Event("#remove_duplicate_files_btn", "click", () => Api("remove_duplicate_files_api"));
Event("#log-btn", "click", async () => {
  document.querySelector("main").innerHTML = `<div>${await getData("../static/info.log", "text")}</div>`
})
