// Common JavaScript functions for the application

// Student Delete Function
function deleteStudent(button) {
  const studentId = button.getAttribute("data-student-id");
  const studentName = button.getAttribute("data-student-name");

  console.log("Delete Student Called - ID:", studentId, "Name:", studentName);

  // Use SweetAlert2 if available, otherwise fallback to confirm
  if (typeof Swal !== "undefined") {
    Swal.fire({
      title: "حذف الطالب",
      html: `هل أنت متأكد من حذف الطالب "<strong>${studentName}</strong>"؟<br><small class="text-muted">سيتم حذف جميع البيانات المرتبطة به (الحضور والمدفوعات).</small>`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "نعم، احذف",
      cancelButtonText: "إلغاء",
      reverseButtons: true,
    }).then((result) => {
      if (result.isConfirmed) {
        submitForm("POST", `/delete_student/${studentId}`);
      }
    });
  } else {
    // Fallback to simple confirm
    if (
      confirm(
        `هل أنت متأكد من حذف الطالب "${studentName}"؟\n\nسيتم حذف جميع البيانات المرتبطة به (الحضور والمدفوعات).`
      )
    ) {
      submitForm("POST", `/delete_student/${studentId}`);
    }
  }
}

// User Delete Function
function deleteUser(button) {
  const userId = button.getAttribute("data-user-id");
  const userName = button.getAttribute("data-user-name");

  console.log("Delete User Called - ID:", userId, "Name:", userName);

  // Use SweetAlert2 if available, otherwise fallback to confirm
  if (typeof Swal !== "undefined") {
    Swal.fire({
      title: "هل أنت متأكد؟",
      html: `سيتم حذف المستخدم "<strong>${userName}</strong>" نهائياً`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "نعم، احذف",
      cancelButtonText: "إلغاء",
      reverseButtons: true,
    }).then((result) => {
      if (result.isConfirmed) {
        submitForm("POST", `/delete_user/${userId}`);
      }
    });
  } else {
    // Fallback to simple confirm
    if (confirm(`هل أنت متأكد من حذف المستخدم "${userName}"؟`)) {
      submitForm("POST", `/delete_user/${userId}`);
    }
  }
}

// Generic form submission function
function submitForm(method, action, data = {}) {
  console.log("Submitting form - Method:", method, "Action:", action);

  const form = document.createElement("form");
  form.method = method;
  form.action = action;
  form.style.display = "none";

  // Add any additional data as hidden inputs
  for (const [key, value] of Object.entries(data)) {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = key;
    input.value = value;
    form.appendChild(input);
  }

  document.body.appendChild(form);
  form.submit();
}

// General purpose confirmation dialog
function confirmAction(
  title,
  message,
  confirmText = "نعم",
  cancelText = "إلغاء"
) {
  return new Promise((resolve) => {
    if (typeof Swal !== "undefined") {
      Swal.fire({
        title: title,
        text: message,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        reverseButtons: true,
      }).then((result) => {
        resolve(result);
      });
    } else {
      // Fallback to browser confirm
      const confirmed = confirm(`${title}\n\n${message}`);
      resolve({ isConfirmed: confirmed });
    }
  });
}

// Show success message
function showSuccess(title, message) {
  if (typeof Swal !== "undefined") {
    Swal.fire({
      title: title,
      text: message,
      icon: "success",
      confirmButtonText: "موافق",
    });
  } else {
    alert(`${title}\n${message}`);
  }
}

// Show error message
function showError(title, message) {
  if (typeof Swal !== "undefined") {
    Swal.fire({
      title: title,
      text: message,
      icon: "error",
      confirmButtonText: "موافق",
    });
  } else {
    alert(`${title}\n${message}`);
  }
}

// Debug function to test if everything is working
function testDeleteFunctions() {
  console.log("Testing delete functions...");
  console.log("SweetAlert2 available:", typeof Swal !== "undefined");
  console.log("jQuery available:", typeof $ !== "undefined");
  console.log("Bootstrap available:", typeof bootstrap !== "undefined");
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log("Common.js loaded successfully");
  // Uncomment the line below for debugging
  // testDeleteFunctions();
});
