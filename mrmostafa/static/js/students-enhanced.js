// Enhanced Students Table JavaScript Functions
// تحسينات جدول الطلاب مع الـ scroll والفلاتر

document.addEventListener("DOMContentLoaded", function () {
  console.log("Students page enhanced JavaScript loaded");

  // Initialize all functions
  initializeFilters();
  initializeEnhancedTable();
  initializeBulkActions();

  console.log("All students page features initialized");
});

// Filter Functions
function submitFilter() {
  console.log("Submitting filter...");
  const form = document.getElementById("filterForm");
  if (form) {
    form.submit();
  } else {
    console.error("Filter form not found");
  }
}

function clearFilters() {
  console.log("Clearing filters...");
  const groupFilter = document.getElementById("group_filter");
  const ageFilter = document.getElementById("age_filter");
  const locationFilter = document.getElementById("location_filter");

  if (groupFilter) groupFilter.value = "";
  if (ageFilter) ageFilter.value = "";
  if (locationFilter) locationFilter.value = "";

  const form = document.getElementById("filterForm");
  if (form) {
    form.submit();
  } else {
    console.error("Filter form not found");
  }
}

function initializeFilters() {
  console.log("Initializing filters...");

  // Add event listeners for filter dropdowns
  const groupFilter = document.getElementById("group_filter");
  const ageFilter = document.getElementById("age_filter");
  const locationFilter = document.getElementById("location_filter");

  if (groupFilter) {
    groupFilter.addEventListener("change", submitFilter);
    console.log("Group filter event listener added");
  }
  if (ageFilter) {
    ageFilter.addEventListener("change", submitFilter);
    console.log("Age filter event listener added");
  }
  if (locationFilter) {
    locationFilter.addEventListener("change", submitFilter);
    console.log("Location filter event listener added");
  }
}

// Enhanced Table Scrolling Functions
function initializeEnhancedTable() {
  console.log("Initializing enhanced table...");

  const topScrollBar = document.getElementById("topScrollBar");
  const tableContainer = document.getElementById("tableContainer");
  const scrollContent = topScrollBar
    ? topScrollBar.querySelector(".scroll-content")
    : null;
  const table = document.getElementById("studentsTable");

  console.log("Table elements status:", {
    topScrollBar: !!topScrollBar,
    tableContainer: !!tableContainer,
    scrollContent: !!scrollContent,
    table: !!table,
  });

  if (!topScrollBar || !tableContainer || !scrollContent || !table) {
    console.warn("Some table elements missing, skipping enhanced table setup");
    return;
  }

  // Set up top scroll bar width to match table width
  function updateScrollContent() {
    const tableWidth = table.scrollWidth;
    const containerWidth = tableContainer.clientWidth;

    console.log("Updating scroll content:", {
      tableWidth: tableWidth,
      containerWidth: containerWidth,
      needsScroll: tableWidth > containerWidth,
    });

    scrollContent.style.width = tableWidth + "px";

    // Show/hide top scroll bar based on whether horizontal scrolling is needed
    if (tableWidth > containerWidth) {
      topScrollBar.style.display = "block";
      console.log("Top scroll bar shown");
    } else {
      topScrollBar.style.display = "none";
      console.log("Top scroll bar hidden");
    }
  }

  // Synchronize scrolling between top bar and table
  let isTopScrolling = false;
  let isTableScrolling = false;

  topScrollBar.addEventListener("scroll", function () {
    if (!isTableScrolling) {
      isTopScrolling = true;
      tableContainer.scrollLeft = this.scrollLeft;
      console.log("Top scroll synced to table:", this.scrollLeft);
      setTimeout(() => {
        isTopScrolling = false;
      }, 50);
    }
  });

  tableContainer.addEventListener("scroll", function () {
    if (!isTopScrolling) {
      isTableScrolling = true;
      topScrollBar.scrollLeft = this.scrollLeft;
      console.log("Table scroll synced to top:", this.scrollLeft);
      setTimeout(() => {
        isTableScrolling = false;
      }, 50);
    }
  });

  // Column toggle functionality
  const columnToggles = {
    "toggle-phone": ".col-phone",
    "toggle-age": ".col-age",
    "toggle-location": ".col-location",
    "toggle-price": ".col-price",
    "toggle-discount": ".col-discount",
    "toggle-final-price": ".col-final-price",
    "toggle-paid": ".col-paid",
    "toggle-remaining": ".col-remaining",
    "toggle-date": ".col-date",
  };

  // Set up column toggles
  Object.keys(columnToggles).forEach((toggleId) => {
    const toggle = document.getElementById(toggleId);
    if (toggle) {
      toggle.addEventListener("change", function () {
        const columns = document.querySelectorAll(columnToggles[toggleId]);
        console.log(
          `Toggling column ${toggleId}:`,
          this.checked,
          `(${columns.length} columns)`
        );

        columns.forEach((col) => {
          if (this.checked) {
            col.classList.remove("hidden");
          } else {
            col.classList.add("hidden");
          }
        });

        // Update scroll content width after column visibility change
        setTimeout(updateScrollContent, 100);
      });
      console.log(`Column toggle ${toggleId} initialized`);
    }
  });

  // Update scroll content on window resize
  window.addEventListener("resize", function () {
    setTimeout(updateScrollContent, 100);
  });

  // Initial setup
  setTimeout(() => {
    updateScrollContent();
    console.log("Enhanced table initialization complete");
  }, 500);
}

// Bulk Actions Functions
function initializeBulkActions() {
  console.log("Initializing bulk actions...");

  // Add event listeners for bulk selection
  const selectAllCheckbox = document.getElementById("select-all");
  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener("change", function () {
      const studentCheckboxes = document.querySelectorAll(".student-checkbox");
      const isChecked = this.checked;

      studentCheckboxes.forEach((checkbox) => {
        checkbox.checked = isChecked;
        const studentId = parseInt(checkbox.value);
        toggleStudentSelection(studentId, isChecked);
      });
      console.log("Select all toggled:", isChecked);
    });
  }

  // Add event listeners for individual student checkboxes
  document.querySelectorAll(".student-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      const studentId = parseInt(this.value);
      toggleStudentSelection(studentId, this.checked);
    });
  });
}

// Quick Search Function
function quickSearch() {
  const searchText = document.getElementById("search_text").value.toLowerCase();
  const table = document.querySelector("table tbody");
  const rows = table.querySelectorAll("tr");
  let visibleCount = 0;

  console.log("Quick search for:", searchText);

  rows.forEach((row) => {
    if (row.cells.length > 1) {
      // Skip empty state row
      const studentName = row.cells[2].textContent.toLowerCase(); // Student name is in third column (after checkbox and #)
      if (studentName.includes(searchText)) {
        row.style.display = "";
        visibleCount++;
      } else {
        row.style.display = "none";
      }
    }
  });

  // Update count badge
  const badge = document.querySelector(".badge.bg-info");
  if (badge) {
    badge.innerHTML = `<i class="fas fa-list-ol me-1"></i>عدد النتائج: ${visibleCount}`;
  }

  console.log("Search results:", visibleCount, "visible rows");
}

function clearSearch() {
  document.getElementById("search_text").value = "";
  quickSearch();
}

// Export Functions
function exportFiltered() {
  console.log("Exporting filtered data...");

  const students = [];
  const table = document.querySelector("table tbody");
  const rows = table.querySelectorAll('tr:not([style*="display: none"])'); // Only visible rows

  // Add header
  students.push([
    "#",
    "الاسم",
    "الهاتف",
    "العمر",
    "المنطقة",
    "المجموعات",
    "سعر الكورس",
    "المبلغ المدفوع",
    "المتبقي",
    "تاريخ التسجيل",
  ]);

  rows.forEach((row, index) => {
    if (row.cells.length > 1) {
      // Skip empty state row
      const cells = Array.from(row.cells).slice(1, -1); // Exclude checkbox and actions columns
      const rowData = cells.map((cell) => cell.textContent.trim());
      students.push(rowData);
    }
  });

  if (students.length > 1) {
    const csvContent = students.map((row) => row.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "students_filtered.csv");
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    if (typeof showSuccess === "function") {
      showSuccess("تم التصدير بنجاح", "تم تحميل ملف البيانات بنجاح");
    }
    console.log("Export completed successfully");
  } else {
    if (typeof showError === "function") {
      showError("لا توجد بيانات", "لا توجد بيانات للتصدير");
    }
    console.log("No data to export");
  }
}

// WhatsApp Function
function openWhatsApp(phoneNumber) {
  console.log("Opening WhatsApp for:", phoneNumber);

  // Remove all non-digit characters except + at the beginning
  let cleanPhone = phoneNumber.replace(/[^\d+]/g, "");

  // If phone doesn't start with +, assume it's an Egyptian number and add +20
  if (!cleanPhone.startsWith("+")) {
    // Remove leading zero if present for Egyptian numbers
    if (cleanPhone.startsWith("0")) {
      cleanPhone = cleanPhone.substring(1);
    }
    cleanPhone = "+20" + cleanPhone;
  }

  // Open WhatsApp
  const whatsappUrl = `https://wa.me/${cleanPhone}`;
  window.open(whatsappUrl, "_blank");
  console.log("WhatsApp URL opened:", whatsappUrl);
}

// Global functions for use in inline HTML
window.submitFilter = submitFilter;
window.clearFilters = clearFilters;
window.quickSearch = quickSearch;
window.clearSearch = clearSearch;
window.exportFiltered = exportFiltered;
window.openWhatsApp = openWhatsApp;
