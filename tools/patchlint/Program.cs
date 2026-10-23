// Checks every [HarmonyPatch] in the compiled mod against the game's code, without running the game:
// each patch must resolve to exactly one method (an ambiguous or missing target makes the game's
// PatchAll abort, which silently disables the other patches).
// Usage: dotnet run -- <mod.dll> <game Managed dir>
using System.Reflection;

var modDll = args[0];
var managed = args[1];
var paths = Directory.GetFiles(managed, "*.dll").ToList();
paths.Add(modDll);
paths.AddRange(Directory.GetFiles(Path.GetDirectoryName(typeof(object).Assembly.Location)!, "*.dll")
    .Where(p => !paths.Any(q => Path.GetFileName(q) == Path.GetFileName(p))));
using var mlc = new MetadataLoadContext(new PathAssemblyResolver(paths), "mscorlib");
var mod = mlc.LoadFromAssemblyPath(modDll);
int failures = 0, checkedCount = 0;
const BindingFlags All = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static;

foreach (var type in mod.GetTypes())
{
    foreach (var attr in type.CustomAttributes.Where(a => a.AttributeType.Name == "HarmonyPatch"))
    {
        var ctorArgs = attr.ConstructorArguments;
        if (ctorArgs.Count < 2 || ctorArgs[0].Value is not Type target || ctorArgs[1].Value is not string name)
        {
            Console.WriteLine($"SKIP  {type.Name}: unsupported HarmonyPatch form");
            continue;
        }
        Type[] argTypes = ctorArgs.Count > 2 && ctorArgs[2].Value is IReadOnlyCollection<CustomAttributeTypedArgument> list
            ? list.Select(a => (Type)a.Value!).ToArray() : null;
        var candidates = new List<MethodInfo>();
        for (var t = target; t != null; t = t.BaseType)
        {
            candidates.AddRange(t.GetMethods(All | BindingFlags.DeclaredOnly).Where(m => m.Name == name));
            if (candidates.Count > 0) break; // AccessTools stops at the most-derived declaring type
        }
        if (argTypes != null)
            candidates = candidates.Where(m => m.GetParameters().Select(p => p.ParameterType.FullName)
                .SequenceEqual(argTypes.Select(a => a.FullName))).ToList();
        checkedCount++;
        if (candidates.Count == 1)
        {
            // Harmony injects patch parameters by name: every non-"__" parameter must exist on the target.
            var targetParams = candidates[0].GetParameters().Select(p => p.Name).ToHashSet();
            foreach (var pm in type.GetMethods(All | BindingFlags.DeclaredOnly).Where(m => m.Name is "Prefix" or "Postfix"))
                foreach (var p in pm.GetParameters().Where(p => !p.Name!.StartsWith("__") && !targetParams.Contains(p.Name)))
                {
                    failures++;
                    Console.WriteLine($"FAIL  {type.Name}.{pm.Name}: parameter '{p.Name}' not on target");
                }
        }
        if (candidates.Count == 1)
            Console.WriteLine($"OK    {type.Name} -> {target.Name}.{name}({string.Join(", ", candidates[0].GetParameters().Select(p => p.ParameterType.Name))})");
        else
        {
            failures++;
            Console.WriteLine($"FAIL  {type.Name} -> {target.Name}.{name}: {candidates.Count} matches" +
                (argTypes == null ? " (no argument types given)" : ""));
        }
    }
}
Console.WriteLine($"{checkedCount} patches checked, {failures} failed");
return failures == 0 ? 0 : 1;
