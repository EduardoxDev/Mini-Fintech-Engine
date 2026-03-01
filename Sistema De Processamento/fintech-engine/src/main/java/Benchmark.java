
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

public class Benchmark {
    public static void main(String[] args) throws Exception {
        System.out.println("Starting Benchmark...");
        ExecutorService executor = Executors.newFixedThreadPool(10);
        HttpClient client = HttpClient.newHttpClient();

        for (int i = 0; i < 100; i++) {
            executor.submit(() -> {
                try {
                    String json = "{\"sourceId\":\"1\",\"targetId\":\"2\",\"amount\":10}";
                    HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:8080/api/transfers"))
                        .header("Content-Type", "application/json")
                        .header("Idempotency-Key", UUID.randomUUID().toString())
                        .POST(HttpRequest.BodyPublishers.ofString(json))
                        .build();
                    client.send(request, HttpResponse.BodyHandlers.ofString());
                } catch (Exception e) {}
            });
        }
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES);
        System.out.println("Benchmark Finished");
    }
}
