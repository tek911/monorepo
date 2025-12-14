package com.vulnmonolith.auth.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.StringReader;

/**
 * VULNERABILITY: XXE (XML External Entity) Processing
 * CWE-611: Improper Restriction of XML External Entity Reference
 */
@RestController
@RequestMapping("/api/xml")
public class XmlController {

    /**
     * VULNERABILITY: XXE - External entities enabled
     * Allows reading local files and SSRF via XML external entities
     */
    @PostMapping(value = "/parse", consumes = "application/xml")
    public ResponseEntity<?> parseXml(@RequestBody String xmlData) {
        try {
            // VULNERABILITY: DocumentBuilderFactory with XXE enabled
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            // All of these should be disabled but aren't:
            // factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
            // factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
            // factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.parse(new InputSource(new StringReader(xmlData)));

            // Return parsed content
            NodeList nodes = document.getDocumentElement().getChildNodes();
            StringBuilder result = new StringBuilder();
            for (int i = 0; i < nodes.getLength(); i++) {
                result.append(nodes.item(i).getTextContent()).append("\n");
            }

            return ResponseEntity.ok(result.toString());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("XML parsing error: " + e.getMessage());
        }
    }

    /**
     * VULNERABILITY: XXE in user import functionality
     */
    @PostMapping(value = "/import-users", consumes = "application/xml")
    public ResponseEntity<?> importUsers(@RequestBody String xmlData) {
        try {
            // VULNERABILITY: Same XXE issue in "business" endpoint
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.parse(new InputSource(new StringReader(xmlData)));

            NodeList users = document.getElementsByTagName("user");
            int imported = users.getLength();

            return ResponseEntity.ok("Imported " + imported + " users");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Import failed: " + e.getMessage());
        }
    }

    /**
     * Example XXE payload for testing:
     *
     * <?xml version="1.0" encoding="UTF-8"?>
     * <!DOCTYPE foo [
     *   <!ENTITY xxe SYSTEM "file:///etc/passwd">
     * ]>
     * <user>
     *   <name>&xxe;</name>
     * </user>
     */
}
