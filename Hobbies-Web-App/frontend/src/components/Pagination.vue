<template>
    <nav aria-label="Pagination" class="mt-4">
        <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="$emit('change-page', currentPage - 1)">Previous</button>
            </li>
            <li class="page-item" v-for="page in visiblePages" :key="page"
                :class="{ active: page === currentPage, disabled: page === '...' }">
                <button v-if="page !== '...'" class="page-link" @click="$emit('change-page', page)">
                    {{ page }}
                </button>
                <span v-else class="page-link">...</span>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="$emit('change-page', currentPage + 1)">Next</button>
            </li>
        </ul>
    </nav>
</template>

<script>
export default {
    name: "Pagination",
    props: {
        currentPage: {
            type: Number,
            required: true,
        },
        totalPages: {
            type: Number,
            required: true,
        },
        siblingCount: {
            type: Number,
            default: 1,
        },
    },
    computed: {
        visiblePages() {
            const { currentPage, totalPages, siblingCount } = this;
            const totalNumbers = siblingCount * 2 + 5;

            if (totalPages <= totalNumbers) {
                return Array.from({ length: totalPages }, (_, i) => i + 1);
            }

            const leftSiblingIndex = Math.max(currentPage - siblingCount, 1);
            const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages);

            const showLeftDots = leftSiblingIndex > 2;
            const showRightDots = rightSiblingIndex < totalPages - 1;

            const pages = [];

            if (showLeftDots) {
                pages.push(1, '...');
            } else {
                pages.push(...Array.from({ length: leftSiblingIndex - 1 }, (_, i) => i + 1));
            }

            pages.push(
                ...Array.from({ length: rightSiblingIndex - leftSiblingIndex + 1 }, (_, i) => leftSiblingIndex + i)
            );

            if (showRightDots) {
                pages.push('...', totalPages);
            } else {
                pages.push(...Array.from({ length: totalPages - rightSiblingIndex }, (_, i) => rightSiblingIndex + 1));
            }

            return pages;
        },
    },
};
</script>