// Ambiguous Java syntax that may confuse parsers
// WARNING: This file contains intentionally confusing code

package com.vulnmonolith.stress;

import java.util.*;
import java.util.function.*;

public class ambiguous_syntax {

    // Generic type with confusing nested angle brackets
    Map<String, Map<String, List<Map<String, Set<Map<String, List<String>>>>>>> nestedGenerics;

    // Confusing lambda syntax
    Function<Function<Integer, Function<Integer, Integer>>, Function<Integer, Integer>> confusingLambda =
        f -> x -> f.apply(y -> y).apply(x);

    // Diamond operator confusion
    Map<String, List<? extends Comparable<? super String>>> diamondConfusion = new HashMap<>();

    // Method with confusing generics
    public <T extends Comparable<? super T> & Serializable> List<? extends T> confusingMethod(
        Collection<? super T> input,
        Comparator<? super T> comparator,
        Function<? super T, ? extends String> mapper
    ) {
        // VULNERABILITY: SQL Injection (hidden in confusing code)
        String query = "SELECT * FROM users WHERE id = '" + input.toString() + "'";
        return null;
    }

    // Nested class confusion
    class Outer {
        class Inner {
            class Deeper {
                class Deepest {
                    // VULNERABILITY: Hardcoded password
                    String password = "secret123";
                }
            }
        }

        static class StaticInner {
            // Confusing static nested class
        }
    }

    // Anonymous class inception
    Object confusingAnonymous = new Object() {
        Object inner = new Object() {
            Object deeper = new Object() {
                // VULNERABILITY hidden deep
                String apiKey = "sk_live_xxxxxxxxxxxx";
            };
        };
    };

    // Confusing ternary chains
    int ternaryMadness = true ? false ? 1 : true ? 2 : 3 : false ? 4 : true ? 5 : 6;

    // Unicode identifiers
    int π = 3;
    String 你好 = "hello";
    double Δ = 0.001;

    // Operator confusion
    void operators() {
        int i = 0;
        int j = i+++i;  // i++ + i or i + ++i?
        int k = i---i;  // i-- - i or i - --i?
        int l = i+++++i; // Multiple increments
    }

    // String with escape sequences
    String escapes = "line1\nline2\ttab\\backslash\"quote\'apostrophe\r\nwindows\u0000null";

    // Multi-line strings (Java 15+)
    String textBlock = """
        This is a text block
        with "quotes" and 'apostrophes'
        and a password = 'hidden_secret_123'
        and an api_key = "sk_live_test"
        """;

    // Confusing method reference syntax
    Consumer<String> methodRef = System.out::println;
    Supplier<List<String>> constructorRef = ArrayList::new;
    Function<String[], List<String>> arrayMethodRef = Arrays::asList;

    // Varargs confusion
    void varargs(String... args) {}
    void varargs(String first, String... rest) {}

    // Confusing array syntax
    int[] array1;
    int array2[];
    int[] array3, array4[];
    String[][] matrix1;
    String[] matrix2[];
    String matrix3[][];

    // Labeled statements (rarely used)
    void labeledStatements() {
        outerLoop:
        for (int i = 0; i < 10; i++) {
            innerLoop:
            for (int j = 0; j < 10; j++) {
                if (j == 5) break outerLoop;
                if (i == 3) continue innerLoop;
            }
        }
    }

    // Instance initializer confusion
    {
        // Instance initializer block
        // VULNERABILITY: Eval-like behavior
        Runtime.getRuntime().exec("echo vulnerable");
    }

    // Static initializer
    static {
        // Static initializer block
        System.setProperty("password", "static_secret_123");
    }
}
