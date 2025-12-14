import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { darkPurple, lightGreen } from '../../constants/colors';

const bgPage = '#F5F7FB';
const card = '#FFFFFF';
const cardSoft = '#F6F7FB';
const border = '#E5E7EB';
const borderStrong = '#D1D5DB';
const text = '#0F172A';
const muted = '#6B7280';
const muted2 = '#9CA3AF';
const accent = darkPurple;
const accentAlt = '#0F766E';
const warning = '#F59E0B';
const danger = '#EF4444';
const success = '#16A34A';

const shadowSm = '0 10px 40px rgba(15, 23, 42, 0.08)';
const shadowSoft = '0 30px 80px rgba(15, 23, 42, 0.06)';

export const Container = styled.div`
  min-height: 100vh;
  background: radial-gradient(120% 60% at 20% 10%, #e9e2ff 0%, rgba(233, 226, 255, 0) 60%),
    radial-gradient(100% 40% at 80% 0%, #d8f5ef 0%, rgba(216, 245, 239, 0) 60%),
    ${bgPage};
  display: flex;
  flex-direction: column;
`;

// HEADER
export const Header = styled.header`
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(14px);
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 1px solid ${border};
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
`;

export const HeaderContent = styled.div`
  height: 72px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 16px;
`;

export const LogoImage = styled.img`
  height: 34px;
  width: auto;
`;

export const NavMenu = styled.nav`
  display: flex;
  gap: 8px;
  justify-self: center;
  background: rgba(241, 245, 249, 0.6);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid ${border};
`;

export const NavItem = styled(Link)`
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: ${(props) => (props.$active ? accent : muted)};
  background: ${(props) => (props.$active ? '#FFFFFF' : 'transparent')};
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  box-shadow: ${(props) => (props.$active ? '0 2px 8px rgba(0,0,0,0.04)' : 'none')};

  &:hover {
    color: ${accent};
    background: ${(props) => (props.$active ? '#FFFFFF' : 'rgba(255,255,255,0.5)')};
  }
`;

export const UserProfile = styled(Link)`
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: right;
  border-left: 1px solid ${border};
  padding-left: 16px;
  text-decoration: none;
  cursor: pointer;
  color: inherit;

  &:hover {
    opacity: 0.8;
  }
`;

export const UserName = styled.div`
  font-weight: 800;
  font-size: 13px;
  color: ${text};
  line-height: 1.1;
`;

export const UserRole = styled.div`
  font-size: 12px;
  color: ${muted};
  line-height: 1.1;
`;

export const UserAvatar = styled.img`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
`;

// MAIN
export const MainContent = styled.main`
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 20px 48px;
  display: flex;
  flex-direction: column;
  gap: 24px;

  @media (min-width: 768px) {
    padding: 40px 20px 56px;
    gap: 28px;
  }
`;

export const TopBar = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: ${muted};
`;

export const SectionBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(106, 58, 159, 0.1);
  color: ${accent};
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.01em;
  text-transform: uppercase;
`;

export const SectionMeta = styled.span`
  font-size: 13px;
  font-weight: 700;
  color: ${muted};
`;

export const ActionSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;

  @media (min-width: 768px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
  }
`;

export const PageHeader = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

export const PageTitle = styled.h1`
  font-size: 30px;
  color: ${text};
  font-weight: 900;
  margin: 0;
  letter-spacing: -0.03em;

  @media (min-width: 768px) {
    font-size: 34px;
  }
`;

export const PageSubtitle = styled.p`
  margin: 0;
  font-size: 15px;
  color: ${muted};
  line-height: 1.35;
  max-width: 760px;

  @media (min-width: 768px) {
    font-size: 15px;
  }
`;

export const CreateButton = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: linear-gradient(120deg, ${accent}, #8b5cf6);
  color: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 12px 18px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease;
  box-shadow: ${shadowSm};

  &:hover {
    transform: translateY(-1px);
    opacity: 0.98;
  }

  &:active {
    transform: translateY(0);
    opacity: 0.95;
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.24), ${shadowSm};
  }
`;

export const GhostButton = styled.button`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid ${borderStrong};
  background: rgba(255, 255, 255, 0.8);
  font-weight: 800;
  color: ${text};
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    border-color: ${accent};
    box-shadow: ${shadowSm};
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.18), ${shadowSm};
  }
`;

// STATS
export const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;

  @media (min-width: 640px) {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
`;

export const StatCard = styled.div`
  background: ${card};
  border-radius: 16px;
  padding: 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid ${border};
  border-left: 6px solid ${(props) => props.$borderColor || lightGreen};
  box-shadow: ${shadowSm};
  transition: transform 0.14s ease, box-shadow 0.14s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${shadowSoft};
  }
`;

export const StatIconWrapper = styled.div`
  width: 46px;
  height: 46px;
  background: linear-gradient(135deg, rgba(106, 58, 159, 0.12), rgba(14, 165, 233, 0.12));
  border: 1px solid rgba(106, 58, 159, 0.16);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${accent};
`;

export const StatInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2px;
`;

export const StatTitle = styled.span`
  font-size: 13px;
  color: ${muted};
  font-weight: 700;
`;

export const StatValue = styled.span`
  font-size: 30px;
  font-weight: 900;
  color: ${text};
  letter-spacing: -0.02em;
`;

// FILTERS
export const FiltersBar = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 4px;

  @media (min-width: 768px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
  }
`;

export const FiltersRow = styled.div`
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
`;

export const SearchInputWrapper = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  background: ${card};
  border: 1px solid ${border};
  border-radius: 14px;
  padding: 0 14px;
  height: 48px;
  width: 100%;
  max-width: 460px;
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.02);

  &:focus-within {
    border-color: rgba(107, 46, 158, 0.35);
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.14);
  }
`;

export const SearchInput = styled.input`
  border: none;
  outline: none;
  flex: 1;
  font-size: 14px;
  color: ${text};
  background: transparent;

  &::placeholder {
    color: ${muted2};
    font-weight: 600;
  }
`;

export const FilterSelect = styled.select`
  height: 46px;
  padding: 0 14px;
  border-radius: 12px;
  border: 1px solid ${border};
  background: ${card};
  color: ${text};
  font-size: 14px;
  font-weight: 700;
  outline: none;
  min-width: 180px;
  cursor: pointer;
  transition: box-shadow 0.12s ease, border-color 0.12s ease;

  &:focus-visible {
    border-color: rgba(107, 46, 158, 0.35);
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.14);
  }
`;

// TABLE WRAPPER
export const TableCard = styled.section`
  background: ${card};
  border: 1px solid ${border};
  border-radius: 18px;
  box-shadow: ${shadowSoft};
  padding: 18px;

  @media (min-width: 768px) {
    padding: 20px;
  }
`;

export const TableContainer = styled.div`
  width: 100%;
  overflow-x: auto;
  border-radius: 14px;
  border: 1px solid ${border};
  background: ${cardSoft};
`;

const tableCols = '0.5fr 1.5fr 2fr 1fr 1fr 1fr';

export const TableHeader = styled.div`
  display: grid;
  grid-template-columns: ${tableCols};
  padding: 14px 16px;
  background-color: ${cardSoft};
  border-bottom: 1px solid ${border};
  font-weight: 800;
  color: ${text};
  font-size: 13px;
  min-width: 900px;
`;

export const TableRow = styled.div`
  display: grid;
  grid-template-columns: ${tableCols};
  padding: 16px;
  align-items: center;
  border-bottom: 1px solid ${border};
  min-width: 900px;
  background: ${card};
  transition: background 0.12s ease, transform 0.12s ease;

  &:hover {
    background-color: #f8f9fb;
    transform: translateY(-1px);
  }

  &:last-child {
    border-bottom: none;
  }
`;

export const IdBadge = styled.div`
  width: 42px;
  height: 42px;
  background-color: rgba(106, 58, 159, 0.08);
  color: ${accent};
  border: 1px solid rgba(107, 46, 158, 0.14);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 13px;
`;

export const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 3px;
`;

export const UserTitle = styled.span`
  font-weight: 900;
  color: ${text};
  font-size: 14px;
  letter-spacing: -0.01em;
`;

export const UserMeta = styled.span`
  font-size: 12px;
  color: ${muted};
  font-weight: 700;
`;

export const StatusBadge = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 900;
  width: fit-content;

  background-color: ${(props) =>
    props.$status === 'ativo' || props.$status === 'published'
      ? 'rgba(34, 197, 94, 0.14)'
      : props.$status === 'inativo'
      ? 'rgba(239, 68, 68, 0.12)'
      : 'rgba(245, 158, 11, 0.16)'};
  color: ${(props) =>
    props.$status === 'ativo' || props.$status === 'published'
      ? success
      : props.$status === 'inativo'
      ? danger
      : warning};
  border: 1px solid rgba(0, 0, 0, 0.04);
`;

export const ActionButton = styled.button`
  justify-self: end;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 38px;
  padding: 0 14px;
  border-radius: 12px;
  border: 1px solid ${border};
  background: ${card};
  color: ${text};
  font-weight: 800;
  font-size: 13px;
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    border-color: ${accent};
    box-shadow: ${shadowSm};
    color: ${accent};
  }

  &:active {
    transform: translateY(0px);
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.14);
  }
`;

// DRAWER / DETAILS
export const DrawerOverlay = styled.div`
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.35);
  display: grid;
  place-items: center;
  z-index: 30;
`;

export const DrawerPanel = styled.div`
  width: min(540px, 92%);
  background: ${card};
  border: 1px solid ${border};
  box-shadow: ${shadowSoft};
  border-radius: 16px;
  padding: 24px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

export const DrawerHeader = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: flex-start;
`;

export const DrawerTitle = styled.h3`
  margin: 0;
  font-size: 20px;
  font-weight: 900;
  color: ${text};
`;

export const DrawerSub = styled.span`
  font-size: 12px;
  color: ${muted};
  font-weight: 800;
`;

export const DrawerContent = styled.div`
  display: grid;
  gap: 10px;
  padding: 10px 0;
`;

export const DrawerRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 10px;
  border-bottom: 1px dashed ${border};
  padding: 6px 0;
`;

export const DrawerLabel = styled.span`
  font-size: 12px;
  color: ${muted};
  font-weight: 800;
`;

export const DrawerValue = styled.span`
  font-size: 14px;
  color: ${text};
  font-weight: 800;
`;

export const Tag = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 900;
  background: ${(p) =>
    p.$tone === 'ativo'
      ? 'rgba(22, 163, 74, 0.14)'
      : p.$tone === 'inativo'
      ? 'rgba(239, 68, 68, 0.12)'
      : 'rgba(245, 158, 11, 0.16)'};
  color: ${(p) =>
    p.$tone === 'ativo' ? success : p.$tone === 'inativo' ? danger : warning};
  border: 1px solid rgba(0, 0, 0, 0.04);
`;

export const DrawerActions = styled.div`
  margin-top: 8px;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
`;

export const PillButton = styled.button`
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid ${(p) => (p.$primary ? accent : border)};
  background: ${(p) => (p.$primary ? `linear-gradient(120deg, ${accent}, #8b5cf6)` : card)};
  color: ${(p) => (p.$primary ? '#fff' : text)};
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: ${shadowSm};
    border-color: ${accent};
  }
`;

export const InsightCard = styled.div`
  border: 1px solid ${border};
  border-radius: 14px;
  background: ${cardSoft};
  padding: 12px;
  display: grid;
  gap: 6px;
`;

export const InsightTitle = styled.div`
  font-weight: 900;
  color: ${text};
`;

export const InsightList = styled.ul`
  margin: 0;
  padding-left: 16px;
  display: grid;
  gap: 6px;
  color: ${muted};
  font-weight: 700;
  font-size: 13px;
`;

export const InsightItem = styled.li`
  line-height: 1.4;
`;

// EMPTY STATE
export const EmptyState = styled.div`
  padding: 36px 20px;
  text-align: center;
  display: grid;
  gap: 10px;
  place-items: center;
  background: linear-gradient(135deg, rgba(106, 58, 159, 0.06), rgba(15, 118, 110, 0.06));
`;

export const EmptyTitle = styled.h3`
  margin: 0;
  font-size: 18px;
  color: ${text};
  font-weight: 900;
`;

export const EmptyText = styled.p`
  margin: 0;
  font-size: 14px;
  max-width: 420px;
  color: ${muted};
  line-height: 1.45;
`;

// PAGINATION
export const PaginationWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  gap: 12px;

  @media (min-width: 768px) {
    flex-direction: row;
  }
`;

export const ResultsText = styled.span`
  color: ${muted};
  font-size: 13px;
  font-weight: 700;

  strong {
    color: ${text};
    font-weight: 900;
  }
`;

export const PageButton = styled.button`
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid ${border};
  background-color: ${(props) => (props.$active ? 'rgba(106, 58, 159, 0.12)' : card)};
  color: ${(props) => (props.$active ? accent : muted)};
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.12s ease, border-color 0.12s ease, box-shadow 0.12s ease;

  &:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    border-color: rgba(107, 46, 158, 0.25);
    box-shadow: ${shadowSm};
    color: ${accent};
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.14);
  }
`;
