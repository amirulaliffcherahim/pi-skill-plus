// Static overview of the imported program. Read-only: changes nothing.
// @category RE
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;

public class RE_Overview extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Program p = currentProgram;
        println("RE_PROGRAM " + p.getName() + " | " + p.getLanguageID() + " | " + p.getCompilerSpec().getCompilerSpecID());
        println("RE_IMAGE_BASE " + p.getImageBase());
        println("RE_FUNCTIONS " + p.getFunctionManager().getFunctionCount());

        int n = 0;
        for (Symbol s : p.getSymbolTable().getExternalSymbols()) {
            if (monitor.isCancelled() || n >= 300) break;
            println("RE_IMPORT " + s.getParentNamespace().getName() + "!" + s.getName());
            n++;
        }

        n = 0;
        DataIterator it = p.getListing().getDefinedData(true);
        while (it.hasNext() && n < 200 && !monitor.isCancelled()) {
            Data d = it.next();
            if (d.hasStringValue()) {
                String v = String.valueOf(d.getValue());
                if (v.length() >= 4) {
                    println("RE_STRING " + d.getAddress() + " " + v.replace("\n", "\\n"));
                    n++;
                }
            }
        }
    }
}
