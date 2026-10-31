from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

import folium


def create_coordinate_map(latitude: float, longitude: float) -> Path:
    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180.")

    coordinate_map = folium.Map(location=[latitude, longitude], zoom_start=13)
    folium.Marker(
        location=[latitude, longitude],
        tooltip="Selected coordinates",
        popup=f"Latitude: {latitude}, Longitude: {longitude}",
    ).add_to(coordinate_map)

    output_path = Path(__file__).with_name("coordinate_map.html")
    coordinate_map.save(output_path)
    return output_path


def serve_coordinate_map(output_path: Path) -> None:
    class CoordinateMapHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path not in ("/", f"/{output_path.name}"):
                self.send_error(404)
                return

            content = output_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    with ThreadingHTTPServer(("127.0.0.1", 0), CoordinateMapHandler) as server:
        map_url = f"http://127.0.0.1:{server.server_port}/{output_path.name}"
        print(f"Serving map at {map_url} (press Ctrl+C to stop)")
        webbrowser.open(map_url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nMap server stopped.")


def main() -> None:
    try:
        latitude = float(input("Enter latitude: "))
        longitude = float(input("Enter longitude: "))
        output_path = create_coordinate_map(latitude, longitude)
    except ValueError as error:
        print(f"Invalid coordinates: {error}")
        return

    serve_coordinate_map(output_path)


if __name__ == "__main__":
    main()