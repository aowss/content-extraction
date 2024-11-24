import org.apache.pdfbox.Loader;
import org.apache.pdfbox.io.RandomAccessReadBufferedFile;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.FileWriter;

class Main {
    private static String pageHeader(int pageNumber) {
        var header = String.format("page %d:", pageNumber);
        var result = ( pageNumber == 1 ? "" : "\n\n" ) + header + "\n";
        for (int i = 0; i < header.length(); ++i) {
            result += "-";
        }
        result += "\n\n";
        return result;
    }

    public static void main(String[] args) throws Exception {
        File inputFile = new File("resources/in/ISCC-Sample-1.pdf");
        File oututFile = new File("resources/out/ISCC-Sample-1-pdfbox-sorted.txt");

        PDFTextStripper stripper = new PDFTextStripper();
        stripper.setSortByPosition(true);

        try (PDDocument document = Loader.loadPDF(new RandomAccessReadBufferedFile(inputFile));
             var output = new FileWriter(oututFile)) {
            String result = "";
            for (int p = 1; p <= document.getNumberOfPages(); ++p) {
                stripper.setStartPage(p);
                stripper.setEndPage(p);
                result += pageHeader(p);
                result += stripper.getText(document).trim();
            }
            output.write(result);
//            PDDocumentCatalog catalog = document.getDocumentCatalog();
//            PDAcroForm form = catalog.getAcroForm();
//            List<PDField> fields = form.getFields();
//
//            for(PDField field: fields) {
//                Object value = field.getValueAsString();
//                String name = field.getFullyQualifiedName();
//                System.out.print(name);
//                System.out.print(" = ");
//                System.out.print(value);
//                System.out.println();
//            }
//            for (PDPage page : document.getPages()) {
//                // process
//            }
        }
    }
}