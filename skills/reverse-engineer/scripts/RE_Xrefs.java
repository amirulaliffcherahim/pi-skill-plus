// List references to a function name or address (arg). Read-only.
// @category RE
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.util.*;

public class RE_Xrefs extends GhidraScript {
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            println("RE_ERROR usage: RE_Xrefs.java <name|0xaddr>");
            return;
        }
        List<Address> targets = new ArrayList<>();
        if (args[0].startsWith("0x")) {
            targets.add(toAddr(args[0]));
        } else {
            for (Symbol s : currentProgram.getSymbolTable().getSymbols(args[0])) targets.add(s.getAddress());
        }
        if (targets.isEmpty()) {
            println("RE_NOTFOUND " + args[0]);
            return;
        }
        FunctionManager fm = currentProgram.getFunctionManager();
        for (Address t : targets) {
            println("RE_TARGET " + t);
            int n = 0;
            for (Reference r : currentProgram.getReferenceManager().getReferencesTo(t)) {
                if (monitor.isCancelled() || n >= 200) break;
                Function f = fm.getFunctionContaining(r.getFromAddress());
                println("RE_XREF " + r.getFromAddress() + " " + r.getReferenceType()
                    + " in " + (f != null ? f.getName() : "(no function)"));
                n++;
            }
        }
    }
}
