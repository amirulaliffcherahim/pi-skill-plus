// Decompile functions by name or address (arg). No arg: first 20 functions. Read-only.
// @category RE
import ghidra.app.decompiler.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import java.util.*;

public class RE_Decompile extends GhidraScript {
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        List<Function> targets = new ArrayList<>();
        FunctionManager fm = currentProgram.getFunctionManager();

        if (args.length == 0) {
            for (Function f : fm.getFunctions(true)) {
                if (targets.size() >= 20) break;
                targets.add(f);
            }
        } else {
            String q = args[0];
            if (q.startsWith("0x")) {
                Address a = toAddr(q);
                Function f = fm.getFunctionContaining(a);
                if (f != null) targets.add(f);
            } else {
                for (Function f : fm.getFunctions(true)) {
                    if (f.getName().equals(q)) targets.add(f);
                }
            }
        }
        if (targets.isEmpty()) {
            println("RE_NOTFOUND " + (args.length > 0 ? args[0] : "(no functions)"));
            return;
        }

        DecompInterface di = new DecompInterface();
        try {
            if (!di.openProgram(currentProgram)) {
                println("RE_ERROR decompiler failed to open: " + di.getLastMessage());
                return;
            }
            for (Function f : targets) {
                if (monitor.isCancelled()) break;
                DecompileResults r = di.decompileFunction(f, 60, monitor);
                println("RE_FUNC " + f.getName() + " @ " + f.getEntryPoint());
                if (r.decompileCompleted()) {
                    for (String line : r.getDecompiledFunction().getC().split("\n")) println("RE_C " + line);
                } else {
                    println("RE_ERROR " + f.getName() + ": " + r.getErrorMessage());
                }
            }
        } finally {
            di.dispose();
        }
    }
}
