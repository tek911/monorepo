<?php
/**
 * Search Page
 * WARNING: INTENTIONALLY VULNERABLE
 *
 * VULNERABILITIES:
 * - SQL Injection
 * - Reflected XSS
 * - Second-order SQL Injection
 */

require_once 'config.php';
require_once 'includes/functions.php';

$search_term = isset($_GET['q']) ? $_GET['q'] : '';
$category = isset($_GET['category']) ? $_GET['category'] : '';
$sort = isset($_GET['sort']) ? $_GET['sort'] : 'name';
$order = isset($_GET['order']) ? $_GET['order'] : 'ASC';

$results = array();

if ($search_term) {
    // VULNERABILITY: SQL Injection in multiple places
    $query = "SELECT * FROM products
              WHERE name LIKE '%$search_term%'
              OR description LIKE '%$search_term%'";

    if ($category) {
        // VULNERABILITY: SQL Injection in category
        $query .= " AND category = '$category'";
    }

    // VULNERABILITY: SQL Injection in ORDER BY
    $query .= " ORDER BY $sort $order";

    $result = mysqli_query($GLOBALS['db'], $query);

    if ($result) {
        while ($row = mysqli_fetch_assoc($result)) {
            $results[] = $row;
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Search Products</title>
</head>
<body>
    <h1>Search Products</h1>

    <form method="GET" action="">
        <input type="text" name="q" value="<?php echo $search_term; ?>" placeholder="Search...">
        <!-- VULNERABILITY: XSS in value attribute -->

        <select name="category">
            <option value="">All Categories</option>
            <option value="electronics" <?php echo $category == 'electronics' ? 'selected' : ''; ?>>Electronics</option>
            <option value="clothing" <?php echo $category == 'clothing' ? 'selected' : ''; ?>>Clothing</option>
        </select>

        <select name="sort">
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="created_at">Date</option>
        </select>

        <select name="order">
            <option value="ASC">Ascending</option>
            <option value="DESC">Descending</option>
        </select>

        <button type="submit">Search</button>
    </form>

    <div class="results">
        <!-- VULNERABILITY: Reflected XSS -->
        <h2>Results for: <?php echo $search_term; ?></h2>

        <?php if (count($results) > 0): ?>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Price</th>
                        <th>Category</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($results as $product): ?>
                        <tr>
                            <!-- VULNERABILITY: Stored XSS if product data is malicious -->
                            <td><?php echo $product['name']; ?></td>
                            <td><?php echo $product['description']; ?></td>
                            <td>$<?php echo $product['price']; ?></td>
                            <td><?php echo $product['category']; ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php else: ?>
            <p>No results found for "<?php echo $search_term; ?>"</p>
        <?php endif; ?>
    </div>

    <!-- VULNERABILITY: SQL query exposed in debug mode -->
    <?php if (isset($_GET['debug'])): ?>
        <pre>Query: <?php echo $query; ?></pre>
    <?php endif; ?>
</body>
</html>
