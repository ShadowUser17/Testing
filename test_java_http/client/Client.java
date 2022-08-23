import java.net.URI;
import java.net.http.*;

class Client {
    public static void main(String[] args) throws Exception {
        for(int it = 0; it < args.length; it++) {
            var req = HttpRequest.newBuilder().uri(URI.create(args[it])).build();
            var client = HttpClient.newHttpClient();
            var resp = client.send(req, HttpResponse.BodyHandlers.ofString());

            System.out.println("URL: " + args[it]);
            System.out.println("RCode: " + resp.statusCode());
            System.out.println("Body: " + resp.body());
        }
    }
}
