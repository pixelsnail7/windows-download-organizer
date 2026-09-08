/**
 * Register delegated event listener.
 *
 * @param {string} selector CSS selector.
 * @param {string} event Event name.
 * @param {(event: Event) => void} handler Callback function.
 */
function Event(selector, event, handler) {
  document.body.addEventListener(
    event,
    (e) => {
      const targetElement = e.target.closest(selector);
      if (targetElement) {
        handler.call(targetElement, e);
      }
    },
    { capture: true },
  );
}


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
Event("#remove_duplicate_files_btn", "click", () => Api("remove_duplicate_files"));

