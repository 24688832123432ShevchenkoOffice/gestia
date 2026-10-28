"""Англійські тексти юридичних сторінок. Структура розділів збігається з legal_copy."""

from __future__ import annotations


def offer_doc() -> dict:
    return {
        "slug": "offer",
        "title": "Public Contract (Offer)",
        "seo_title": "Public Contract (Offer) · Gestia Home",
        "seo_description": (
            "Public offer of the Gestia Home online store: terms of ordering, payment, delivery, and returns."
        ),
        "sections": [
            {
                "heading": "1. General provisions",
                "paragraphs": [
                    "1.1. This document is a public proposal (offer) of the seller Gestia Home (the \"Seller\") to conclude a contract for the retail sale and purchase of goods at a distance, on the terms set out below.",
                    "1.2. The offer is accepted when the Buyer places an order on the website, confirms the order, and/or pays for the goods. From the moment of acceptance, the contract is deemed concluded.",
                    "1.3. By placing an order, the Buyer confirms that they have read the terms of the offer, the privacy policy, and the cookie policy, and agrees to them.",
                ],
            },
            {
                "heading": "2. Subject of the contract",
                "paragraphs": [
                    "2.1. The Seller undertakes to transfer ownership of the goods to the Buyer, and the Buyer undertakes to accept the goods and pay for them on the terms of this contract.",
                    "2.2. The name, characteristics, availability, and price of the goods are those stated on the relevant page of the website catalogue at the time the order is placed.",
                    "2.3. Images of the goods are illustrative. Insignificant differences in shade, texture, and the items included are permitted because of the nature of the materials and of handmade work.",
                ],
            },
            {
                "heading": "3. Price and payment",
                "paragraphs": [
                    "3.1. Prices are shown in hryvnias (UAH) or euros (EUR), according to the display currency selected on the website. The final amount is fixed at the moment the order is confirmed.",
                    "3.2. The available methods of payment are payment by card online on the website and/or payment on delivery, according to the options available at checkout.",
                    "3.3. The cost of delivery is not included in the price of the goods unless expressly stated otherwise, and is paid according to the carrier's tariffs.",
                ],
            },
            {
                "heading": "4. Placing and fulfilling an order",
                "paragraphs": [
                    "4.1. To place an order, the Buyer provides a name, a telephone number, an email address (if required), and the delivery details.",
                    "4.2. After receiving an order, the Seller may contact the Buyer to clarify the details. The order is deemed accepted once the Seller has confirmed it.",
                    "4.3. The time needed to prepare the order depends on the availability of the goods and on the workshop's workload, and is communicated to the Buyer when the order is confirmed.",
                    "4.4. The Seller may refuse to process an order if the goods are unavailable, if there is an error in the price or the description, or if fraud is suspected, and shall notify the Buyer.",
                ],
            },
            {
                "heading": "5. Delivery",
                "paragraphs": [
                    "5.1. Delivery is performed by delivery services (in particular, Nova Poshta) to a branch, a parcel locker, or by courier, at the Buyer's choice.",
                    "5.2. The indicative delivery time after dispatch is 1–3 business days, unless the parties agree otherwise.",
                    "5.3. The risk of accidental damage to or loss of the goods passes to the Buyer when the goods are handed over to the carrier, unless otherwise provided by law.",
                    "5.4. The Buyer must inspect the integrity of the packaging upon receipt. In the event of damage, a report must be drawn up with a representative of the carrier.",
                ],
            },
            {
                "heading": "6. Returns and exchanges",
                "paragraphs": [
                    "6.1. Returns and exchanges of goods of proper quality are carried out in accordance with the Law of Ukraine \"On Consumer Rights Protection\".",
                    "6.2. Goods made to an individual order, or goods that show signs of use or of damage for which the Buyer is at fault, may not be subject to return, to the extent permitted by law.",
                    "6.3. To make a return, the Buyer contacts the Seller using the contact details on the website. A refund is made by the same method of payment, or by another agreed method, after the goods have been received and checked.",
                ],
            },
            {
                "heading": "7. Liability of the parties",
                "paragraphs": [
                    "7.1. The parties are liable in accordance with the legislation of Ukraine.",
                    "7.2. The Seller is not liable for delays caused by the acts of the carrier, by force majeure, or by the Buyer providing incorrect contact or address details.",
                    "7.3. The Buyer is responsible for the accuracy of the details given when the order is placed.",
                ],
            },
            {
                "heading": "8. Other terms",
                "paragraphs": [
                    "8.1. The Seller may change the terms of the offer. The new version takes effect from the moment it is published on the website, in respect of orders placed after that publication.",
                    "8.2. All disputes shall be resolved by negotiation and, if that is not possible, in the manner prescribed by the legislation of Ukraine.",
                    "8.3. For questions about orders, please use the contact details given in the \"Contacts\" section of the Gestia Home website.",
                ],
            },
        ],
    }


def privacy_doc() -> dict:
    return {
        "slug": "privacy",
        "title": "Privacy Policy",
        "seo_title": "Privacy Policy · Gestia Home",
        "seo_description": (
            "How Gestia Home collects, uses, and protects the personal data of customers and visitors to the website."
        ),
        "sections": [
            {
                "heading": "1. Who we are and what this policy governs",
                "paragraphs": [
                    "1.1. This Privacy Policy explains how Gestia Home (\"we\", the \"Seller\") processes the personal data of users of the website and of customers.",
                    "1.2. Processing is carried out in accordance with the Law of Ukraine \"On Personal Data Protection\" and other applicable rules.",
                    "1.3. By using the website, placing an order, or sending a request, you confirm that you have read this policy.",
                ],
            },
            {
                "heading": "2. What data we collect",
                "paragraphs": [
                    "2.1. Data you provide yourself: your name, telephone number, email address, delivery address, the text of a message, the goods you select, and the parameters of the order.",
                    "2.2. Technical data: IP address, browser type, cookie data, and the time at which pages are visited, to the extent necessary for the operation of the website and for analytics.",
                    "2.3. We do not ask for data we do not need. Form fields are limited to the information required in order to contact you and to fulfil the order.",
                ],
            },
            {
                "heading": "3. Purpose of processing",
                "paragraphs": [
                    "3.1. Placing, confirming, and fulfilling orders; delivery; and communication regarding the status of an order.",
                    "3.2. Replying to enquiries sent through the feedback forms and \"Order now\".",
                    "3.3. Improving the operation of the website, preventing fraud, and complying with legal requirements (record-keeping and tax obligations).",
                    "3.4. We do not transfer your data to third parties for their own advertising.",
                ],
            },
            {
                "heading": "4. Legal grounds",
                "paragraphs": [
                    "4.1. Your consent (in particular, the checkbox consenting to the processing of personal data in the forms).",
                    "4.2. Conclusion and performance of the contract of sale and purchase (the offer).",
                    "4.3. The Seller's legitimate interests — the security of the service and the prevention of abuse — to the extent that those interests do not infringe your rights.",
                ],
            },
            {
                "heading": "5. To whom data may be transferred",
                "paragraphs": [
                    "5.1. To delivery services, so that the order can be handed over.",
                    "5.2. To payment providers, if online payment is selected.",
                    "5.3. To hosting and infrastructure contractors that keep the website in operation, subject to confidentiality being maintained.",
                    "5.4. To state authorities, only in the cases and to the extent provided by law.",
                ],
            },
            {
                "heading": "6. Storage and protection",
                "paragraphs": [
                    "6.1. Data are retained for the period necessary to fulfil the order, to meet warranty and accounting obligations, and to resolve disputes, and for no longer than the law or the purpose of processing requires.",
                    "6.2. We apply organisational and technical measures to protect data against unauthorised access, alteration, or destruction.",
                    "6.3. Data are transmitted over the network using secure connections (HTTPS), where this is technically provided for.",
                ],
            },
            {
                "heading": "7. Your rights",
                "paragraphs": [
                    "7.1. You have the right to know which of your data are being processed, and to require that they be corrected, blocked, or deleted, within the limits of the law.",
                    "7.2. You may withdraw consent to processing by writing to the workshop's contact address or telephone number. Withdrawal does not affect the lawfulness of processing that took place before the withdrawal.",
                    "7.3. Withdrawal of consent may make it impossible to fulfil an order that has not been completed, or to reply to an enquiry.",
                ],
            },
            {
                "heading": "8. Cookies and third-party services",
                "paragraphs": [
                    "8.1. The website uses cookies and similar technologies. The details are set out in the Cookie Policy.",
                    "8.2. Certain services (for example, analytics or payment widgets) may process technical data in accordance with their own policies.",
                ],
            },
            {
                "heading": "9. Changes to the policy",
                "paragraphs": [
                    "9.1. We may update this policy. The current version is always available on this page, together with the date of the update.",
                    "9.2. For questions about personal data, please use the \"Contacts\" section of the Gestia Home website.",
                ],
            },
        ],
    }


def cookies_doc() -> dict:
    return {
        "slug": "cookies",
        "title": "Cookie Policy",
        "seo_title": "Cookie Policy · Gestia Home",
        "seo_description": (
            "Which cookies the Gestia Home website uses, why they are needed, and how to manage the settings."
        ),
        "sections": [
            {
                "heading": "1. What cookies are",
                "paragraphs": [
                    "1.1. Cookies are small text files that are stored in your browser when you visit the Gestia Home website.",
                    "1.2. Similar technologies (local storage and session storage) may be used for the same purpose, namely to keep the website working.",
                ],
            },
            {
                "heading": "2. Why we use cookies",
                "paragraphs": [
                    "2.1. Necessary cookies — for the basket, the wishlist, the language, the currency, the session, and the security of forms (including CSRF).",
                    "2.2. Functional cookies — to remember your interface preferences.",
                    "2.3. Analytics cookies (if they are enabled) — to understand how the website is used and to improve it. Gestia Home does not use them for third parties' advertising.",
                ],
            },
            {
                "heading": "3. Which types of cookies may be used",
                "paragraphs": [
                    "3.1. Session cookies — deleted when you close the browser.",
                    "3.2. Persistent cookies — stored for a defined period, or until you delete them.",
                    "3.3. First-party cookies — set by our website.",
                    "3.4. Third-party cookies — may be set by connected services (payments, analytics, or fonts) if those services are active on the page.",
                ],
            },
            {
                "heading": "4. Examples of necessary cookies on the website",
                "paragraphs": [
                    "4.1. The Django session identifier — authenticated and session-based flows, the basket, and the wishlist.",
                    "4.2. The language cookie — storing the interface language you have selected.",
                    "4.3. The CSRF token — protecting forms against forged requests.",
                    "4.4. Display-currency data — held in the session or in related browser storage.",
                ],
            },
            {
                "heading": "5. How to manage cookies",
                "paragraphs": [
                    "5.1. You may restrict or delete cookies in your browser settings. Instructions are usually found in the \"Privacy\" section.",
                    "5.2. Disabling necessary cookies may cause the basket, the order forms, and the language and currency switch to work incorrectly.",
                    "5.3. On mobile devices, cookie controls are available in the settings of the relevant browser (Safari, Chrome, and others).",
                ],
            },
            {
                "heading": "6. Consent",
                "paragraphs": [
                    "6.1. By continuing to use the website, you agree to the use of the necessary cookies required for the basic operation of the service.",
                    "6.2. If we enable optional analytics or marketing cookies, we will give a separate notice and, where required, ask for your consent.",
                ],
            },
            {
                "heading": "7. Updates to the policy",
                "paragraphs": [
                    "7.1. We may update the Cookie Policy. The current version is published on this page, with the date of the update.",
                    "7.2. Questions about cookies and personal data may be sent through the form in the \"Contacts\" section.",
                ],
            },
        ],
    }


def shipping_doc() -> dict:
    return {
        "slug": "shipping",
        "title": "Delivery and Payment",
        "seo_title": "Delivery and Payment · Gestia Home",
        "seo_description": (
            "Delivery and payment terms for Gestia Home orders: Nova Poshta, courier, online payment, and payment on delivery."
        ),
        "sections": [
            {
                "heading": "1. General terms",
                "paragraphs": [
                    "1.1. This page describes the methods of delivery and payment for orders in the Gestia Home store. The detailed contractual terms are also set out in the Public Contract (Offer).",
                    "1.2. When placing an order, the Buyer chooses a convenient method of delivery and of payment from those available on the website at the time of checkout.",
                    "1.3. The prices of the goods are displayed in the selected currency (UAH or EUR). The final amount is fixed when the order is confirmed.",
                ],
            },
            {
                "heading": "2. Delivery",
                "paragraphs": [
                    "2.1. Delivery is carried out by Nova Poshta within the territory of Ukraine.",
                    "2.2. The available options are a Nova Poshta branch, a Nova Poshta parcel locker, and courier delivery to an address.",
                    "2.3. The indicative delivery time after the order is handed to the carrier is 1–3 business days. The actual time depends on the region and on the carrier's workload.",
                    "2.4. The cost of delivery is calculated according to the carrier's tariffs and is usually paid by the Buyer separately upon receipt, unless otherwise agreed.",
                    "2.5. After dispatch, the Seller provides the consignment note number (TTN) so that the parcel can be tracked.",
                    "2.6. How long a parcel is stored at a branch or a parcel locker is governed by Nova Poshta's rules. Please collect your order in time.",
                ],
            },
            {
                "heading": "3. Receiving the order",
                "paragraphs": [
                    "3.1. On receipt, please check that the packaging is intact. If there is damage, record it with a representative of the carrier (a report) and notify Gestia Home.",
                    "3.2. Claims concerning the contents of the order or visible defects are accepted within a reasonable time after receipt, together with a photograph and a description.",
                    "3.3. If the Buyer has provided incorrect delivery details, a further shipment may be charged for separately.",
                ],
            },
            {
                "heading": "4. Payment",
                "paragraphs": [
                    "4.1. Online by card on the website — Visa / Mastercard through a payment provider (if that method is active at checkout).",
                    "4.2. Payment on delivery — according to the carrier's terms and the availability of this method for the particular order.",
                    "4.3. Payment against bank details may be offered by a manager after the order has been confirmed.",
                    "4.4. The Seller's obligation to dispatch the goods arises after the order has been confirmed and, where required, after payment has been received, depending on the method chosen.",
                ],
            },
            {
                "heading": "5. Preparation of the order",
                "paragraphs": [
                    "5.1. The time needed to prepare the order depends on the availability of the goods and on the workshop's workload. Typical times are confirmed by a manager when the order is confirmed.",
                    "5.2. Handmade goods, or goods made to order, may require additional time to produce. You will be informed of this separately.",
                    "5.3. If an item is unavailable, the Seller will offer a replacement, a wait, or cancellation with a refund (if payment has already been made).",
                ],
            },
            {
                "heading": "6. Refund of delivery charges",
                "paragraphs": [
                    "6.1. The cost of delivery is usually not refunded if a return of goods of proper quality is initiated by the Buyer and the Seller is not at fault, within the limits of the law.",
                    "6.2. If the goods have a manufacturing defect, or if the Seller has made an error in the contents of the order, the question of delivery costs on an exchange or a return is agreed individually.",
                ],
            },
            {
                "heading": "7. Contacts",
                "paragraphs": [
                    "7.1. For questions about delivery and payment, please use the form in the \"Contacts\" section or the telephone number stated on the website.",
                    "7.2. The applicable terms may be updated. The date of the latest update is shown on this page.",
                ],
            },
        ],
    }


DOCS_EN = {
    "offer": offer_doc,
    "privacy": privacy_doc,
    "cookies": cookies_doc,
    "shipping": shipping_doc,
}
