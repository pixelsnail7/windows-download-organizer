export async function getData(url, type = "json") {
  try {
    const request = await fetch(url);

    if (!request.ok) {
      throw new Error(`HTTP error! Status: ${request.status} for ${url}`);
    }

    if (type === "json") {
      return await request.json();
    } else if (type === "text") {
      return await request.text();
    } else {
      throw new Error("Invalid type parameter! Use 'json' or 'text'.");
      return null;
    }
  } catch (e) {
    console.error("Fetch Error:", e.message);
    return null;
  }
}

/**
 * Register delegated event listener.
 *
 * @param {string} selector CSS selector.
 * @param {string} event Event name.
 * @param {(event: Event) => void} handler Callback function.
 */
export function Event(selector, event, handler) {
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
