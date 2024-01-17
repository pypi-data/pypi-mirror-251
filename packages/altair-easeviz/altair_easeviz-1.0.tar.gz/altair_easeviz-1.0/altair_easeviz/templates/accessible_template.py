accesible_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
</head>
<style>
    /* Estilo adicional para las cards */
    .card {
        border: none;
        cursor: pointer;
    }

    .card:hover {
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        transition: all 0.2s;

    }

    .color-palette {
        height: 30px; /* Altura fija para las cards */
    }

    .color-pat-1 {
        background-color: #e41a1c;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='96' viewBox='0 0 60 96'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.64'%3E%3Cpath d='M36 10a6 6 0 0 1 12 0v12a6 6 0 0 1-6 6 6 6 0 0 0-6 6 6 6 0 0 1-12 0 6 6 0 0 0-6-6 6 6 0 0 1-6-6V10a6 6 0 1 1 12 0 6 6 0 0 0 12 0zm24 78a6 6 0 0 1-6-6 6 6 0 0 0-6-6 6 6 0 0 1-6-6V58a6 6 0 1 1 12 0 6 6 0 0 0 6 6v24zM0 88V64a6 6 0 0 0 6-6 6 6 0 0 1 12 0v12a6 6 0 0 1-6 6 6 6 0 0 0-6 6 6 6 0 0 1-6 6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }

    .color-pat-2 {
        background-color: #377eb8;
        background-image: url("data:image/svg+xml,%3Csvg width='12' height='16' viewBox='0 0 12 16' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 .99C4 .445 4.444 0 5 0c.552 0 1 .45 1 .99v4.02C6 5.555 5.556 6 5 6c-.552 0-1-.45-1-.99V.99zm6 8c0-.546.444-.99 1-.99.552 0 1 .45 1 .99v4.02c0 .546-.444.99-1 .99-.552 0-1-.45-1-.99V8.99z' fill='%23000000' fill-opacity='0.77' fill-rule='evenodd'/%3E%3C/svg%3E");

    }

    .color-pat-3 {
        background-color: #4daf4a;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 80 40' width='80' height='40'%3E%3Cpath fill='%23000000' fill-opacity='0.62' d='M0 40a19.96 19.96 0 0 1 5.9-14.11 20.17 20.17 0 0 1 19.44-5.2A20 20 0 0 1 20.2 40H0zM65.32.75A20.02 20.02 0 0 1 40.8 25.26 20.02 20.02 0 0 1 65.32.76zM.07 0h20.1l-.08.07A20.02 20.02 0 0 1 .75 5.25 20.08 20.08 0 0 1 .07 0zm1.94 40h2.53l4.26-4.24v-9.78A17.96 17.96 0 0 0 2 40zm5.38 0h9.8a17.98 17.98 0 0 0 6.67-16.42L7.4 40zm3.43-15.42v9.17l11.62-11.59c-3.97-.5-8.08.3-11.62 2.42zm32.86-.78A18 18 0 0 0 63.85 3.63L43.68 23.8zm7.2-19.17v9.15L62.43 2.22c-3.96-.5-8.05.3-11.57 2.4zm-3.49 2.72c-4.1 4.1-5.81 9.69-5.13 15.03l6.61-6.6V6.02c-.51.41-1 .85-1.48 1.33zM17.18 0H7.42L3.64 3.78A18 18 0 0 0 17.18 0zM2.08 0c-.01.8.04 1.58.14 2.37L4.59 0H2.07z'%3E%3C/path%3E%3C/svg%3E");
    }

    .color-pat-4 {
        background-color: #984ea3;
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23000000' fill-opacity='0.94' fill-rule='evenodd'/%3E%3C/svg%3E");

    }


</style>
<body>
<!-- Color Patterns -->
<svg height="10" width="10" xmlns="http://www.w3.org/2000/svg" version="1.1">
    <defs>
        <!-- Red Heart-->
        <pattern id="red-heart" patternUnits="userSpaceOnUse" width="24" height="24">
            <g stroke-width="0">
                <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#e41a1c" strokewidth="0"></rect>
            </g>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M12 6.00019C10.2006 3.90317 7.19377 3.2551 4.93923 5.17534C2.68468 7.09558 2.36727 10.3061 4.13778 12.5772C5.60984 14.4654 10.0648 18.4479 11.5249 19.7369C11.6882 19.8811 11.7699 19.9532 11.8652 19.9815C11.9483 20.0062 12.0393 20.0062 12.1225 19.9815C12.2178 19.9532 12.2994 19.8811 12.4628 19.7369C13.9229 18.4479 18.3778 14.4654 19.8499 12.5772C21.6204 10.3061 21.3417 7.07538 19.0484 5.17534C16.7551 3.2753 13.7994 3.90317 12 6.00019Z"
                      stroke="#000000" fill="none" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
            </g>
        </pattern>
        <!-- Blue Rain-->
        <pattern id="blue-rain" patternUnits="userSpaceOnUse" width="24" height="24">
            <g stroke-width="0">
                <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#377eb8" strokewidth="0"/>
            </g>
            <g stroke-linecap="round" stroke-linejoin="round"/>
            <g>
                <defs>
                    <style>
                        .cls-1 {
                            fill: none;
                            stroke: #020202;
                            stroke-miterlimit: 10;
                            stroke-width: 1.2;
                        }
                    </style>
                </defs>
                <path class="cls-1" d="M17,19a3.47,3.47,0,0,1-6.94,0c0-3.47,3.47-6.08,3.47-6.08S17,15.56,17,19Z"/>
                <path class="cls-1" d="M22.5,7.35a3.34,3.34,0,1,1-6.68,0c0-3.34,3.34-5.85,3.34-5.85S22.5,4,22.5,7.35Z"/>
                <path class="cls-1"
                      d="M8.18,11.52a3.34,3.34,0,0,1-6.68,0c0-3.34,3.34-5.84,3.34-5.84S8.18,8.18,8.18,11.52Z"/>
            </g>
        </pattern>

        <!-- Green Leaf-->
        <pattern id="green-leaf" patternUnits="userSpaceOnUse" width="24" height="24">
            <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#4daf4a" strokewidth="0"></rect>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path d="M14 10L4 20M20 7C20 12.5228 15.5228 17 10 17C9.08396 17 8.19669 16.8768 7.35385 16.6462C7.12317 15.8033 7 14.916 7 14C7 8.47715 11.4772 4 17 4C17.916 4 18.8033 4.12317 19.6462 4.35385C19.8768 5.19669 20 6.08396 20 7Z"
                      stroke="#000000" fill="none" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
            </g>
        </pattern>
        <!-- Purple Grapes-->
        <pattern id="purple-grapes" patternUnits="userSpaceOnUse" width="24" height="24">
            <g stroke-width="0">
                <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#984ea3" strokewidth="0"></rect>
            </g>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path d="M21,12a5.006,5.006,0,0,0-5-5A4.951,4.951,0,0,0,13,8.03c0-.009.005-.016.005-.025A2.853,2.853,0,0,1,16,5a1,1,0,0,0,0-2,4.709,4.709,0,0,0-3.729,1.54A5.466,5.466,0,0,0,7,1,1,1,0,0,0,6,2,8.362,8.362,0,0,0,7.674,7.033a4.981,4.981,0,0,0-.539,9.88A4.871,4.871,0,0,0,7,18a5,5,0,1,0,9.873-1.088A5,5,0,0,0,21,12ZM10.882,6.851c-1.888-.542-2.539-2.445-2.764-3.7C10.006,3.691,10.657,5.593,10.882,6.851ZM5,12a3,3,0,0,1,6,0C11,15.975,5,15.976,5,12Zm7,9a3,3,0,0,1-3-3,2.868,2.868,0,0,1,.251-1.174A5.049,5.049,0,0,0,11.982,15a3.074,3.074,0,0,1,2.576,1.458A2.98,2.98,0,0,1,12,21Zm4-6h-.018a4.976,4.976,0,0,0-2.64-1.794c-.031-.009-.06-.024-.091-.032A2.868,2.868,0,0,1,13,12a3,3,0,1,1,3,3Z"></path>
            </g>
        </pattern>

        <!-- Orange Orange-->
        <pattern id="orange-orange" patternUnits="userSpaceOnUse" width="24" height="24">
            <g stroke-width="0">
                <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#ff7f00" strokewidth="0"></rect>
            </g>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M12.8596 6.80422C13.1527 5.90212 14.0002 5.25 15 5.25V3.75C13.884 3.75 12.8819 4.23749 12.1949 5.01113C11.6511 4.2478 10.7587 3.75 9.75 3.75H8.25V5.25C8.25 6.08469 8.59088 6.83976 9.14102 7.38359C6.84229 8.45993 5.25 10.794 5.25 13.5C5.25 17.2279 8.27208 20.25 12 20.25C15.7279 20.25 18.75 17.2279 18.75 13.5C18.75 10.0633 16.1816 7.22647 12.8596 6.80422ZM12 8.25C9.10051 8.25 6.75 10.6005 6.75 13.5C6.75 16.3995 9.10051 18.75 12 18.75C14.8995 18.75 17.25 16.3995 17.25 13.5C17.25 10.6005 14.8995 8.25 12 8.25ZM14.25 13.5C14.25 12.2574 13.2426 11.25 12 11.25V9.75C14.0711 9.75 15.75 11.4289 15.75 13.5H14.25ZM11.25 6.75C10.4216 6.75 9.75 6.07843 9.75 5.25C10.5784 5.25 11.25 5.92157 11.25 6.75Z"
                      fill="#000000"></path>
            </g>
        </pattern>
        <!-- Yellow Star-->
        <pattern id="yellow-star" patternUnits="userSpaceOnUse" width="24" height="24">
            <g stroke-width="0">
                <rect x="-2.4" y="-2.4" width="28" height="28" rx="0" fill="#ffff33" strokewidth="0"></rect>
            </g>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path d="M11.2691 4.41115C11.5006 3.89177 11.6164 3.63208 11.7776 3.55211C11.9176 3.48263 12.082 3.48263 12.222 3.55211C12.3832 3.63208 12.499 3.89177 12.7305 4.41115L14.5745 8.54808C14.643 8.70162 14.6772 8.77839 14.7302 8.83718C14.777 8.8892 14.8343 8.93081 14.8982 8.95929C14.9705 8.99149 15.0541 9.00031 15.2213 9.01795L19.7256 9.49336C20.2911 9.55304 20.5738 9.58288 20.6997 9.71147C20.809 9.82316 20.8598 9.97956 20.837 10.1342C20.8108 10.3122 20.5996 10.5025 20.1772 10.8832L16.8125 13.9154C16.6877 14.0279 16.6252 14.0842 16.5857 14.1527C16.5507 14.2134 16.5288 14.2807 16.5215 14.3503C16.5132 14.429 16.5306 14.5112 16.5655 14.6757L17.5053 19.1064C17.6233 19.6627 17.6823 19.9408 17.5989 20.1002C17.5264 20.2388 17.3934 20.3354 17.2393 20.3615C17.0619 20.3915 16.8156 20.2495 16.323 19.9654L12.3995 17.7024C12.2539 17.6184 12.1811 17.5765 12.1037 17.56C12.0352 17.5455 11.9644 17.5455 11.8959 17.56C11.8185 17.5765 11.7457 17.6184 11.6001 17.7024L7.67662 19.9654C7.18404 20.2495 6.93775 20.3915 6.76034 20.3615C6.60623 20.3354 6.47319 20.2388 6.40075 20.1002C6.31736 19.9408 6.37635 19.6627 6.49434 19.1064L7.4341 14.6757C7.46898 14.5112 7.48642 14.429 7.47814 14.3503C7.47081 14.2807 7.44894 14.2134 7.41394 14.1527C7.37439 14.0842 7.31195 14.0279 7.18708 13.9154L3.82246 10.8832C3.40005 10.5025 3.18884 10.3122 3.16258 10.1342C3.13978 9.97956 3.19059 9.82316 3.29993 9.71147C3.42581 9.58288 3.70856 9.55304 4.27406 9.49336L8.77835 9.01795C8.94553 9.00031 9.02911 8.99149 9.10139 8.95929C9.16534 8.93081 9.2226 8.8892 9.26946 8.83718C9.32241 8.77839 9.35663 8.70162 9.42508 8.54808L11.2691 4.41115Z"
                      fill="none" stroke="#000000" stroke-width="1" stroke-linecap="round"></path>
            </g>
        </pattern>
        <!-- Brown Chocolate-->
        <pattern id="brown-chocolate" patternUnits="userSpaceOnUse" width="24" height="24">
            <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#a65628" strokewidth="0"></rect>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path d="M9 8L9 8.01" stroke="#333333" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
                <path d="M16 15L16 15.01" stroke="#333333" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
                <path d="M10 17L10 17.01" stroke="#333333" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
                <path d="M11 13L11 13.01" stroke="#333333" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
                <path d="M6 12L6 12.01" stroke="#333333" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
                <path d="M12 21C16.9706 21 21 16.9706 21 12C21 11.4402 20.9489 10.8924 20.8511 10.361C20.3413 10.7613 19.6985 11 19 11C18.4536 11 17.9413 10.8539 17.5 10.5987C17.0587 10.8539 16.5464 11 16 11C14.3431 11 13 9.65685 13 8C13 7.60975 13.0745 7.23691 13.2101 6.89492C11.9365 6.54821 11 5.38347 11 4C11 3.66387 11.0553 3.34065 11.1572 3.03894C6.58185 3.46383 3 7.31362 3 12C3 16.9706 7.02944 21 12 21Z"
                      fill="none" stroke="#333333" stroke-width="2" stroke-linecap="round"
                      stroke-linejoin="round"></path>
            </g>
        </pattern>
        <!-- Pink Donut-->
        <pattern id="pink-donut" patternUnits="userSpaceOnUse" width="24" height="24">
            <g stroke-width="0">
                <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#f781bf" strokewidth="0"></rect>
            </g>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M2.92362 10.2072C2.8097 10.7872 2.75 11.3866 2.75 12C2.75 12.2264 2.75814 12.451 2.77413 12.6733C2.79516 12.6904 2.81728 12.7083 2.84044 12.7268C3.06058 12.9028 3.37094 13.1369 3.73188 13.3698C4.4894 13.8584 5.33178 14.25 6 14.25C6.43561 14.25 6.9638 14.0813 7.51796 13.8023C7.85469 13.6327 8.17653 13.435 8.46068 13.2423C8.32421 12.8535 8.25 12.4354 8.25 12C8.25 9.92893 9.92893 8.25 12 8.25C14.0711 8.25 15.75 9.92893 15.75 12C15.75 12.771 15.5173 13.4877 15.1183 14.0836C15.3411 14.1896 15.5713 14.25 15.8053 14.25C16.2683 14.25 16.487 14.0308 16.9218 13.516C16.9323 13.5036 16.9429 13.491 16.9537 13.4782C17.3151 13.0495 17.8429 12.4235 18.7798 12.28C18.6514 12.2408 18.532 12.1667 18.4368 12.0586C18.163 11.7477 18.1931 11.2738 18.504 11L20.182 9.52217C20.3764 9.351 20.6345 9.29861 20.8676 9.35938C20.6364 8.58192 20.3058 7.84726 19.8905 7.17018L19.5303 7.53033C19.2374 7.82322 18.7626 7.82322 18.4697 7.53033C18.1768 7.23744 18.1768 6.76256 18.4697 6.46967L18.9936 5.94571C17.2976 3.98821 14.7934 2.75 12 2.75C10.2299 2.75 8.57597 3.24718 7.17018 4.10952L7.53033 4.46967C7.82322 4.76256 7.82322 5.23744 7.53033 5.53033C7.23744 5.82322 6.76256 5.82322 6.46967 5.53033L5.94571 5.00637C4.94045 5.87738 4.12488 6.96151 3.56929 8.18848C3.97987 8.16935 4.32998 8.4847 4.3529 8.89596L4.43156 10.308C4.4546 10.7216 4.13801 11.0755 3.72444 11.0985C3.31086 11.1216 2.95692 10.805 2.93388 10.3914L2.92362 10.2072ZM21.1543 10.6647L19.4953 12.1257C19.4342 12.1795 19.3668 12.2216 19.2958 12.2521C20.0516 12.2809 20.6933 12.5991 21.1987 12.9798C21.2326 12.6578 21.25 12.3309 21.25 12C21.25 11.5465 21.2174 11.1007 21.1543 10.6647ZM20.8507 14.6969C20.4093 14.1984 19.8194 13.75 19.1842 13.75C18.7213 13.75 18.5026 13.9692 18.0677 14.484C18.0573 14.4964 18.0466 14.509 18.0359 14.5218C17.6254 15.0086 17.0005 15.75 15.8053 15.75C15.0981 15.75 14.49 15.4931 14.0034 15.1706C13.4238 15.5375 12.7367 15.75 12 15.75C10.9043 15.75 9.91838 15.2801 9.23274 14.5308C8.92219 14.7382 8.56885 14.9526 8.19255 15.142C7.55133 15.4649 6.77639 15.75 6 15.75C4.98743 15.75 3.95347 15.2623 3.1792 14.7932C4.36349 18.5366 7.86487 21.25 12 21.25C16.1705 21.25 19.6963 18.49 20.8507 14.6969ZM1.25 12C1.25 6.06294 6.06294 1.25 12 1.25C17.9371 1.25 22.75 6.06294 22.75 12C22.75 17.9371 17.9371 22.75 12 22.75C6.06294 22.75 1.25 17.9371 1.25 12ZM10.4697 3.46967C10.7626 3.17678 11.2374 3.17678 11.5303 3.46967L12.5303 4.46967C12.8232 4.76256 12.8232 5.23744 12.5303 5.53033C12.2374 5.82322 11.7626 5.82322 11.4697 5.53033L10.4697 4.53033C10.1768 4.23744 10.1768 3.76256 10.4697 3.46967ZM16.45 4.4C16.7814 4.64853 16.8485 5.11863 16.6 5.45L15.1 7.45C14.8515 7.78137 14.3814 7.84853 14.05 7.6C13.7186 7.35147 13.6515 6.88137 13.9 6.55L15.4 4.55C15.6485 4.21863 16.1186 4.15147 16.45 4.4ZM11.2244 6.80589C11.3317 7.20599 11.0942 7.61724 10.6941 7.72444L9.32809 8.09047C8.92799 8.19768 8.51674 7.96024 8.40953 7.56014C8.30232 7.16004 8.53976 6.74879 8.93986 6.64158L10.3059 6.27556C10.706 6.16835 11.1172 6.40579 11.2244 6.80589ZM5.89686 7.17364C6.27394 7.00223 6.71858 7.16896 6.88999 7.54605L7.47522 8.83349C7.64662 9.21058 7.47989 9.65522 7.10281 9.82662C6.72572 9.99803 6.28108 9.8313 6.10967 9.45422L5.52445 8.16677C5.35304 7.78969 5.51977 7.34505 5.89686 7.17364ZM16.6146 8.22733C17.0284 8.20789 17.3796 8.52754 17.399 8.9413L17.4654 10.3539C17.4849 10.7677 17.1652 11.1189 16.7515 11.1383C16.3377 11.1578 15.9865 10.8381 15.9671 10.4244L15.9007 9.01171C15.8812 8.59796 16.2009 8.24678 16.6146 8.22733ZM12 9.75C10.7574 9.75 9.75 10.7574 9.75 12C9.75 13.2426 10.7574 14.25 12 14.25C13.2426 14.25 14.25 13.2426 14.25 12C14.25 10.7574 13.2426 9.75 12 9.75ZM6.94308 10.8949C7.27734 11.1396 7.34999 11.6089 7.10536 11.9431L6.27012 13.0843C6.02549 13.4186 5.55621 13.4912 5.22195 13.2466C4.88769 13.002 4.81504 12.5327 5.05968 12.1984L5.89491 11.0572C6.13954 10.723 6.60883 10.6503 6.94308 10.8949Z"
                      fill="#000000"></path>
            </g>
        </pattern>
        <!-- Grey Wrench -->
        <pattern id="grey-wrench" patternUnits="userSpaceOnUse" width="24" height="24">
            <rect x="-2.4" y="-2.4" width="28.80" height="28.80" rx="0" fill="#999999" strokewidth="0"></rect>
            <g stroke-linecap="round" stroke-linejoin="round"></g>
            <g>
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M3.5362 5.29854C3.861 5.23721 4.19511 5.34035 4.42884 5.57407L6.90007 8.0453C7.21718 8.36241 7.73131 8.36241 8.04842 8.0453C8.36553 7.7282 8.36553 7.21406 8.04842 6.89695L5.57841 4.42694C5.34457 4.1931 5.24146 3.85877 5.30297 3.53383C5.36449 3.2089 5.58266 2.93539 5.8858 2.8032C8.06696 1.85206 10.7034 2.26698 12.4903 4.05384C13.9041 5.46765 14.4588 7.41411 14.1581 9.24419L21.0366 16.1227C22.3936 17.4796 22.3936 19.6797 21.0366 21.0367C19.6796 22.3936 17.4796 22.3936 16.1226 21.0367L9.24405 14.1581C7.41401 14.4588 5.46762 13.904 4.05384 12.4903C2.26556 10.702 1.85139 8.06276 2.80548 5.88058C2.93789 5.57772 3.2114 5.35986 3.5362 5.29854ZM4.30644 8.2801C4.30858 9.29283 4.69632 10.3043 5.46805 11.076C6.50688 12.1149 7.97927 12.4581 9.30695 12.1009C9.6523 12.008 10.021 12.1066 10.2739 12.3595L17.5368 19.6225C18.1127 20.1984 19.0465 20.1984 19.6224 19.6225C20.1983 19.0466 20.1983 18.1128 19.6224 17.5369L12.3595 10.274C12.1066 10.0211 12.008 9.65241 12.1009 9.30705C12.4582 7.97934 12.1149 6.50691 11.076 5.46805C10.3059 4.69791 9.29699 4.31018 8.28635 4.30645L9.46264 5.48274C10.5608 6.58089 10.5608 8.36136 9.46264 9.45952C8.36448 10.5577 6.58401 10.5577 5.48586 9.45952L4.30644 8.2801Z"
                      fill="#000000"></path>
            </g>
        </pattern>

        <!--Colors from Vega Colors Schemes #dark2 -->
        <!-- Teal Vertical strips -->
        <pattern id="teal-vertical" patternUnits="userSpaceOnUse" width="10" height="10">
            <rect width="10" height="10" fill="#1B9E77"/>
            <rect x="0" y="0" width="3" height="10" fill="white"/>
        </pattern>
        <!-- Orange Horizontal Strips -->
        <pattern id="orange-horizontal" patternUnits="userSpaceOnUse" width="10" height="10">
            <rect width="10" height="10" fill="#D95F02"/>
            <rect x="0" y="0" width="10" height="3" fill="white"/>
        </pattern>
        <!-- Purple Diagonal Strips right to left -->
        <pattern id="purple-diagonal-rl" patternUnits="userSpaceOnUse" width="10" height="10">
            <rect width="10" height="10" fill="#7570B3"/>
            <path d="M-1,1 l2,-2            M0,10 l10,-10            M9,11 l2,-2" stroke="white" stroke-width="1"/>
        </pattern>
        <!-- Pink Diagonal Strips left to right -->
        <pattern id="pink-diagonal-lr" patternUnits="userSpaceOnUse" width="10" height="10">
            <rect width="10" height="10" fill="#E7298A"/>
            <path d="M-1,1 l2,2 M0,0 l10,10 M9,9 l2,2" stroke="white" stroke-width="1"/>
        </pattern>
        <!-- Green Dots Inverted-->
        <pattern id="green-dots-inv" patternUnits="userSpaceOnUse" width="10" height="10">
            <rect width="10" height="10" fill="#66A61E"/>
            <rect x="0" y="0" width="5" height="5" fill="white"/>
        </pattern>
        <!-- Yellow circles -->
        <pattern id="yellow-circles" patternUnits="userSpaceOnUse" width="10" height="10">
            <rect width="10" height="10" fill="#E6AB02"/>
            <circle cx="2.5" cy="2.5" r="2.5" fill="white"/>
        </pattern>
        <!-- Brown CrossHatch -->
        <pattern id="brown-cross" patternUnits="userSpaceOnUse" width="8" height="8">
            <rect width="8" height="8" fill="#A6761D"/>
            <path d="M0 0L8 8ZM8 0L0 8Z" stroke-width="0.5" stroke="#fff"/>
        </pattern>
        <!-- Grey Houndstooth -->
        <pattern id="grey-houndstooth" patternUnits="userSpaceOnUse" width="10" height="10">
            <path d="M0 0L4 4" stroke="#666666" fill="#aaa" stroke-width="1"/>
            <path d="M2.5 0L5 2.5L5 5L9 9L5 5L10 5L10 0" stroke="#666666" fill="#aaa" stroke-width="1"/>
            <path d="M5 10L5 7.5L7.5 10" stroke="#666666" fill="#aaa" stroke-width="1"/>
        </pattern>
    </defs>
</svg>

<!-- Main Body -->
<div class="container mt-3">
    <!-- Selectors for Graph-->
    <div class="row ">
        <div class="col-12">
            <h3>{{title}} </h3>
            <p>The next graph can modified its size and size fonts to be more readable</p>
            <p> {% if multi_chart %}
                <span class="badge badge-danger bg-secondary">This is a layered chart</span>
                {% endif %}Layered and concat charts are not fully supported, reload the page to recover the original
                graph
            </p>
        </div>

        <!-- Color Scheme Selector -->
        <div class="row col-12">
            <div class="col-md-3">
                <div id="cat-palette-1" class="card color-card p-2" tabindex="0">
                    <h5 class="card-title">Categorical Scheme 1</h5>
                    <div class="color-palette"
                         style="background: linear-gradient(90deg, #1b9e77 25%, #d95f02 25%, #d95f02 50%, #7570b3 50%, #7570b3 75%, #e7298a 75%, #e7298a 100%); "></div>

                </div>
            </div>
            <div class="col-md-3">
                <div id="cat-palette-2" class="card color-card p-2 " tabindex="0">
                    <h5 class="card-title">Categorical Scheme 2</h5>
                    <div class="color-palette"
                         style="background: linear-gradient(90deg, #a6cee3 25%, #1f78b4 25%, #1f78b4 50%, #b2df8a 50%, #b2df8a 75%, #33a02c 75%, #33a02c 100%); "></div>

                </div>
            </div>
            <div class="col-md-3">
                <div id="div-palette-1" class="card color-card p-2 " tabindex="0">
                    <h5 class="card-title">Diverging Scheme 1</h5>
                    <div class="color-palette"
                         style="background: linear-gradient(90deg, #543005 25%, #dfc27d 25%, #dfc27d 50%, #80cdc1 50%, #80cdc1 75%, #003c30 75%, #003c30 100%); "></div>

                </div>
            </div>
            <div class="col-md-3">
                <div id="div-palette-2" class="card color-card p-2 " tabindex="0">
                    <h5 class="card-title">Diverging Scheme 2</h5>
                    <div class="color-palette"
                         style="background: linear-gradient(90deg, #40004b 25%, #c2a5cf 25%, #c2a5cf 50%, #a6dba0 50%, #a6dba0 75%, #00441b 75%, #00441b 100%); "></div>
                </div>
            </div>
            <div class="col-md-3">
                <div id="pat-palette-1" class="card color-card p-2" tabindex="0">
                    <h5 class="card-title">Color Pattern</h5>
                    <div class="color-palette row m-2">
                        <div class="col color-pat-1"></div>
                        <div class="col color-pat-2"></div>
                        <div class="col color-pat-3"></div>
                        <div class="col color-pat-4"></div>
                    </div>

                </div>
            </div>
        </div>

    </div>
    <div class="col-12 my-3">
        <!-- Change Text Size -->
        <div class="" role="group" aria-label="Change text size">
            <button id="increaseSizeText" class="btn btn-lg btn-danger">Increase font</button>
            <button id="decreaseSizeText" class="btn btn-lg btn-primary">Decrease font</button>
        </div>
    </div>
    <!-- Height and Width -->
    <div class="col-12">
        <label for="heightGraphInput">Height:</label>
        <input type="range" id="heightGraphInput" min="0" max="1000" value="300" step="10">
        <label for="widthGraphInput">Width:</label>
        <input type="range" id="widthGraphInput" min="0" max="1000" value="300" step="10">
    </div>

    <!-- Accessible Graph -->
    <div class="row my-2">
        <div class="col-12 ">
            <div id="chart"></div>
        </div>
    </div>
    <!-- Chart Description -->
    {% if description_given %}
    <div id="graph-description" class="my-2" tabindex="0">
        <h5 class="px-1">Graph Description</h5>
        <p>{{description_html}}</p>
    </div>
    {% endif %}
</div>

<!-- Basic variables -->
<script>
    const el = document.getElementById('chart');
    const colorSchemes = {
        "dark2": ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666'],
        "paired": ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6'],
        "brownToTeal": ['#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#f5f5f5', '#c7eae5', '#80cdc1', '#35978f', '#01665e'],
        "purple-to-green": ['#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#f7f7f7', '#d9f0d3', '#a6dba0', '#5aae61', '#1b7837'],
        "color-patterns": ["url(#red-heart)", "url(#blue-rain)", "url(#green-leaf)", "url(#purple-grapes)", "url(#orange-orange)",
            "url(#yellow-star)", "url(#brown-chocolate)", "url(#pink-donut)", "url(#grey-wrench)"]
    }
    let fontSizes = {"sm": 12, "md": 14, "lg": 18}
    var $heightGraphInput = $("#heightGraphInput");
    var $widthGraphInput = $("#widthGraphInput");
    var $buttonIncrease = $("#increaseSizeText");
    var $buttonDecrease = $("#decreaseSizeText");
    var $cardCatPalette1 = $("#cat-palette-1");
    var $cardCatPalette2 = $("#cat-palette-2");
    var $cardDivPalette1 = $("#div-palette-1");
    var $cardDivPalette2 = $("#div-palette-2");
    var $cardPatPalette1 = $("#pat-palette-1");

    let spec = {{chart | tojson}};
    let description = `{{ description }}`
    let embedOpt =  { "renderer": "svg" };
    if (!spec.hasOwnProperty("description")) {
        spec.description = description
    }

</script>

<!--  Auxiliar functions-->
<script>
    function showError(el, error) {
        el.innerHTML = ('<div style="color:red;">'
            + '<p>JavaScript Error: ' + error.message + '</p>'
            + "<p>This usually means there's a typo in your chart specification. "
            + "See the javascript console for the full traceback.</p>"
            + '</div>');
        throw error;
    }

    function changeHeight() {
        let newHeight = $heightGraphInput.val();
        spec["height"] = parseInt(newHeight);

        vegaEmbed("#chart", spec, embedOpt).catch(error => showError(el, error));
    }

    function changeWidth() {
        let newWidth = $widthGraphInput.val();
        spec["width"] = parseInt(newWidth)

        vegaEmbed("#chart", spec, embedOpt).catch(error => showError(el, error));
    }

    function changeColorScheme(colorScheme) {
        spec.config['range'] = {...spec.config.range, "category": colorSchemes[colorScheme]}
        vegaEmbed("#chart", spec, embedOpt).catch(error => showError(el, error));
    }

    function biggerFontSize() {
        fontSizes.sm += 2
        fontSizes.md += 2
        fontSizes.lg += 2
        // change axis size
        spec.config['axis'] = {...spec.config.axis, 'labelFontSize': fontSizes.sm, 'titleFontSize': fontSizes.md}
        // change title size
        spec.config['title'] = {...spec.config.title, 'fontSize': fontSizes.lg}
        // change legend size
        spec.config['legend'] = {
            ...spec.config.legend,
            'labelFontSize': fontSizes.sm,
            'titleFontSize': fontSizes.md
        }
        // change text mark size
        spec.config['text'] = {...spec.config.text, 'fontSize': fontSizes.sm}
        // change header size
        spec.config['header'] = {
            ...spec.config.header,
            'labelFontSize': fontSizes.sm,
            'titleFontSize': fontSizes.md
        }


        vegaEmbed("#chart", spec, embedOpt).catch(error => showError(el, error));

    }

    function smallerFontSize() {
        fontSizes.sm -= 2
        fontSizes.md -= 2
        fontSizes.lg -= 2
        // change axis size
        spec.config['axis'] = {...spec.config.axis, 'labelFontSize': fontSizes.sm, 'titleFontSize': fontSizes.md}
        // change title size
        spec.config['title'] = {...spec.config.title, 'fontSize': fontSizes.lg}
        // change legend size
        spec.config['legend'] = {
            ...spec.config.legend,
            'labelFontSize': fontSizes.sm,
            'titleFontSize': fontSizes.md
        }
        // change text mark size
        spec.config['text'] = {...spec.config.text, 'fontSize': fontSizes.sm}
        // change header size
        spec.config['header'] = {
            ...spec.config.header,
            'labelFontSize': fontSizes.sm,
            'titleFontSize': fontSizes.md
        }

        vegaEmbed("#chart", spec, embedOpt).catch(error => showError(el, error));

    }
</script>

<!-- Main sript -->
<script>
    vegaEmbed("#chart", spec, embedOpt).catch(error => showError(el, error));
    $cardCatPalette1.on("click", function () {
        changeColorScheme("dark2")
    });
    $cardCatPalette2.on("click", function () {
        changeColorScheme("paired")
    });
    $cardDivPalette1.on("click", function () {
        changeColorScheme("brownToTeal")
    });
    $cardDivPalette2.on("click", function () {
        changeColorScheme("purple-to-green")
    });
    $cardPatPalette1.on("click", function () {
        changeColorScheme("color-patterns")
    });
    $heightGraphInput.on("input", changeHeight);
    $widthGraphInput.on("input", changeWidth);
    $buttonIncrease.on("click", biggerFontSize);
    $buttonDecrease.on("click", smallerFontSize);
    $cardCatPalette1.on("keydown", function (event) {
        if (event.which === 13) {
            changeColorScheme("dark2")
        }
    });
    $cardCatPalette2.on("keydown", function (event) {
        if (event.which === 13) {
            changeColorScheme("paired")
        }
    });
    $cardDivPalette1.on("keydown", function (event) {
        if (event.which === 13) {
            changeColorScheme("brownToTeal")
        }
    });
    $cardDivPalette2.on("keydown", function (event) {
        if (event.which === 13) {
            changeColorScheme("purple-to-green")
        }
    });
    $cardPatPalette1.on("keydown", function (event) {
        if (event.which === 13) {
            changeColorScheme("color-patterns")
        }
    });
    $buttonIncrease.on("keydown", function (event) {
        if (event.which === 13) {
            biggerFontSize()
        }
    });
    $buttonDecrease.on("keydown", function (event) {
        if (event.which === 13) {
            smallerFontSize()
        }
    });

</script>
</body>
</html>
"""
