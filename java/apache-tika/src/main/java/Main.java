import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.sax.BodyContentHandler;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;

class Main {
    public static void main(String[] args) throws Exception {
        File inputFile = new File("resources/in/ISCC-Sample-1.pdf");
        File oututFile = new File("resources/out/ISCC-Sample-1-tika.txt");

        // Create a Tika parser object
        AutoDetectParser parser = new AutoDetectParser();

        // Create a metadata object to store the document metadata
        Metadata metadata = new Metadata();

        // Create a handler to receive the extracted text
        BodyContentHandler handler = new BodyContentHandler();

        // Create a context object to configure the parser
        ParseContext context = new ParseContext();

        try (var stream = new FileInputStream(inputFile);
             var output = new FileWriter(oututFile)) {

            parser.parse(stream, handler, metadata, context);
            output.write(handler.toString());
        }
    }
}